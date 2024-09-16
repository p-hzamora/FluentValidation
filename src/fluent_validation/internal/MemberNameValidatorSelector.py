from __future__ import annotations
from typing import Iterable, Optional, override, Callable, Any, TYPE_CHECKING
import re

from fluent_validation.MemberInfo import MemberInfo
from fluent_validation.internal.IValidatorSelector import IValidatorSelector


if TYPE_CHECKING:
    from fluent_validation.IValidationRule import IValidationRule
    from fluent_validation.IValidationContext import IValidationContext


class MemberNameValidatorSelector(IValidatorSelector):
    DisableCascadeKey: str = "_FV_DisableSelectorCascadeForChildRules"

    _collectionIndexNormalizer: re.Pattern[str] = re.compile(r"\[.*?\]")

    def __init__(self, memberNames: Iterable[str]):
        self._memberNames: Iterable[str] = memberNames

    @property
    def MemberNames(self) -> Iterable[str]:
        return self._memberNames

    @override
    def CanExecute(self, rule: IValidationRule, propertyPath: str, context: IValidationContext) -> bool:
        from fluent_validation.internal.IncludeRule import IIncludeRule

        # Validator selector only applies to the top level.
        # If we're running in a child context then this means that the child validator has already been selected
        # Because of this, we assume that the rule should continue (ie if the parent rule is valid, all children are valid)
        isChildContext: bool = context.IsChildContext
        cascadeEnabled: bool = self.DisableCascadeKey not in context.RootContextData

        # If a child validator is being executed and the cascade is enabled (which is the default)
        # then the child validator's rule should always be included.
        # The only time this isn't the case is if the member names contained for inclusion are for child
        # properties (which is indicated by them containing a period).
        if isChildContext and cascadeEnabled and not any(["." in x for x in self._memberNames]):
            return True

        if isinstance(rule, IIncludeRule):
            return True

        normalizedPropertyPath: Optional[str] = None

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

    # TODOL: Check if it correct 	public static string[] MemberNamesFromExpressions<T>(params Expression<Func<T, object>>[] propertyExpressions) {

    @classmethod
    def MemberNamesFromExpressions[T](cls, *propertyExpressions: Callable[[T], Any]) -> list[str]:
        members: list[str] = [cls.MemberFromExpression(x) for x in propertyExpressions]
        return members

    @staticmethod
    def MemberFromExpression[T](expression: Callable[[T], Any]) -> str:
        from fluent_validation.ValidatorOptions import ValidatorOptions

        # get list of all values in expression (one is expected) and get first
        propertyName = ValidatorOptions.Global.PropertyNameResolver(type(T), MemberInfo(expression), expression)

        if not propertyName:
            raise ValueError(f"Expression '{expression}' does not specify a valid property or field.")

        return propertyName
