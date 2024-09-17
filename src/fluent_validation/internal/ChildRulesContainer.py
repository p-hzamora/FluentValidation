from typing import Callable
from fluent_validation.InlineValidator import InlineValidator
from fluent_validation.syntax import IRuleBuilderOptions


class ChildRulesContainer[T](InlineValidator[T]):
    """
    /// AbstractValidator implementation for containing child rules.
    """

    def __init__[TProperty](self, *ruleCreator: Callable[[InlineValidator[T]], IRuleBuilderOptions[T, TProperty]]) -> None:
        super().__init__(*ruleCreator)
        self._RuleSetsToApplyToChildRules: list[str] = None

    @property
    def RuleSetsToApplyToChildRules(self) -> list[str]:
        """
        Used to keep track of rulesets from parent that need to be applied
        to child rules in the case of multiple nested child rules.
        """
        # cref="DefaultValidatorExtensions.child_rules{T,TProperty}"
        return self._RuleSetsToApplyToChildRules

    @RuleSetsToApplyToChildRules.setter
    def RuleSetsToApplyToChildRules(self, value: list[str]):
        self._RuleSetsToApplyToChildRules = value
