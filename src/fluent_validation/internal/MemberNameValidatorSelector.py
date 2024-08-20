import re

from src.FluentValidation.IValidationContext import IValidationContext
from src.FluentValidation.IValidationRule import IValidationRule
from src.FluentValidation.internal.IValidatorSelector import IValidatorSelector
from typing import Iterable, override

class MemberNameValidatorSelector(IValidatorSelector):
    DisableCascadeKey:str = "_FV_DisableSelectorCascadeForChildRules"
    
    _collectionIndexNormalizer:re.Pattern[str] = re.compile(r"\[.*?\]")

    def __init__(self, memberNames:Iterable[str]):
        self._memberNames:Iterable[str] = memberNames

    @property
    def MemberNames(self)->Iterable[str]:
        return self._memberNames
    

    @override
    def CanExecute (rule: IValidationRule, propertyPath:str, context: IValidationContext)->bool:
        isChildContext:bool = context.IsChildContext
        cascadeEnabled:bool = not context.RootContextData.ContainsKey(DisableCascadeKey)

        if (isChildContext && cascadeEnabled && !_memberNames.Any(x => x.Contains('.'))) {
            return true
        }

        if (rule is IIncludeRule) {
            return true
        }

        string normalizedPropertyPath = null

        foreach (var memberName in _memberNames) {
            if (memberName == propertyPath) {
                return true
            }

            if (propertyPath.StartsWith(memberName + ".")) {
                return true
            }

            if (memberName.StartsWith(propertyPath + ".")) {
                return true
            }

            if (memberName.StartsWith(propertyPath + "[")) {
                return true
            }

            if (memberName.Contains("[]")) {
                if (normalizedPropertyPath == null) {
                    normalizedPropertyPath = _collectionIndexNormalizer.Replace(propertyPath, "[]")
                }

                if (memberName == normalizedPropertyPath) {
                    return true
                }

                if (memberName.StartsWith(normalizedPropertyPath + ".")) {
                    return true
                }

                if (memberName.StartsWith(normalizedPropertyPath + "[")) {
                    return true
                }
            }
        }

        return false
    }

    static string[] MemberNamesFromExpressions<T>(params Expression<Func<T, object>>[] propertyExpressions) {
        var members = propertyExpressions.Select(MemberFromExpression).ToArray()
        return members
    }

    private static string MemberFromExpression<T>(Expression<Func<T, object>> expression) {
        var propertyName = ValidatorOptions.Global.PropertyNameResolver(typeof(T), expression.GetMember(), expression)

        if (string.IsNullOrEmpty(propertyName)) {
            throw new ArgumentException($"Expression '{expression}' does not specify a valid property or field.")
        }

        return propertyName
    }
}
