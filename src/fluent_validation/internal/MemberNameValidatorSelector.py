import re

from src.fluent_validation.IValidationContext import IValidationContext
from src.fluent_validation.IValidationRule import IValidationRule
# from src.fluent_validation.ValidatorOptions import ValidatorOptions
from src.fluent_validation.internal.IValidatorSelector import IValidatorSelector
from typing import Iterable, Optional, override, Callable, Any

from src.fluent_validation.internal.IncludeRule import IIncludeRule

class MemberNameValidatorSelector(IValidatorSelector):
    DisableCascadeKey:str = "_FV_DisableSelectorCascadeForChildRules"
    
    _collectionIndexNormalizer:re.Pattern[str] = re.compile(r"\[.*?\]")

    def __init__(self, memberNames:Iterable[str]):
        self._memberNames:Iterable[str] = memberNames

    @property
    def MemberNames(self)->Iterable[str]:
        return self._memberNames
    

    @override
    def CanExecute (self, rule: IValidationRule, propertyPath:str, context: IValidationContext)->bool:
        # Validator selector only applies to the top level.
        # If we're running in a child context then this means that the child validator has already been selected
        # Because of this, we assume that the rule should continue (ie if the parent rule is valid, all children are valid)
        isChildContext:bool = context.IsChildContext
        cascadeEnabled:bool = self.DisableCascadeKey not in context.RootContextData

        # If a child validator is being executed and the cascade is enabled (which is the default)
		# then the child validator's rule should always be included.
		# The only time this isn't the case is if the member names contained for inclusion are for child
		# properties (which is indicated by them containing a period).
        if isChildContext & cascadeEnabled and not any(["." in x for x in self._memberNames]):
            return True

        if issubclass(rule,IIncludeRule):
            return True

        normalizedPropertyPath:Optional[str] = None

        for memberName in self._memberNames:
            if memberName == propertyPath:
                return True

            if propertyPath.startswith(memberName + "."):
                return True

            if memberName.startswith(propertyPath + "."):
                return True

            if memberName.startswith(propertyPath + "["):
                return True

            if memberName.count("[]"):
                if normalizedPropertyPath is None:
                    normalizedPropertyPath = self._collectionIndexNormalizer.sub(propertyPath, "[]")

                if memberName == normalizedPropertyPath:
                    return True

                if memberName.startswith(normalizedPropertyPath + "."):
                    return True

                if memberName.startswith(normalizedPropertyPath + "["):
                    return True

        return False
    
    #TODOL: Check if it correct 	public static string[] MemberNamesFromExpressions<T>(params Expression<Func<T, object>>[] propertyExpressions) {

    def MemberNamesFromExpressions[T](self, *propertyExpressions:  Callable[[T],Any])->list[str]:
        members:list[str] = [propertyExpressions.Select(self.MemberFromExpression)]
        return members

    @staticmethod
    def MemberFromExpression[T](expression:Callable[[T],Any])->str:
        #TODOH: Implements Disassembler class developed for ormlambda
        propertyName:str = "___"#ValidatorOptions.Global.PropertyNameResolver(, expression.GetMember(), expression)

        if propertyName == "" or propertyName.isspace() or propertyName is None:
            raise ValueError(f"Expression '{expression}' does not specify a valid property or field.")
        
        return propertyName