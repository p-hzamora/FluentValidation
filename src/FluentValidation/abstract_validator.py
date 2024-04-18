from abc import ABC
from typing import Callable

from .results.ValidationResult import ValidationResult
from .IValidationContext import ValidationContext
from .syntax import IRuleBuilder
from .internal.PropertyRule import PropertyRule
from .internal.RuleBuilder import RuleBuilder

from .ValidatorOptions import ValidatorOptions
from .enums import CascadeMode


class AbstractValidator[T](ABC):
    # region constructor
    def __init__(self) -> None:
        self._classLevelCascadeMode: Callable[[], CascadeMode] = lambda: ValidatorOptions.Global.DefaultClassLevelCascadeMode
        self._ruleLevelCascadeMode: Callable[[], CascadeMode] = lambda: ValidatorOptions.Global.DefaultRuleLevelCascadeMode
        self._rules: list[PropertyRule] = []

    # endregion

    # region Private methods
    def internal_validate(self, context: ValidationContext) -> ValidationResult:
        result: ValidationResult = ValidationResult(errors=context.Failures)
        for rule in self._rules:
            rule.ValidateAsync(context)
            if self.ClassLevelCascadeMode == CascadeMode.Stop and len(result.errors) > 0:
                break

        # self.SetExecutedRuleSets(result,context)
        return result

    def SetExecutedRuleSets(self, result: ValidationResult, context: ValidationContext[T]):
        ...
        # result.RuleSetExecuted = RulesetValidatorSelector.DefaultRuleSetNameInArray

    # endregion

    # region Public methods
    def validate(self, instance: T) -> ValidationResult:
        return self.internal_validate(ValidationContext(instance))

    def rule_for[TProperty](self, func: Callable[[T], TProperty]) -> IRuleBuilder[T, TProperty]:  # IRuleBuilderInitial[T,TProperty]:
        rule: PropertyRule[T, TProperty] = PropertyRule.create(func, lambda: self.RuleLevelCascadeMode)
        self._rules.append(rule)
        return RuleBuilder[T, TProperty](rule, self)

    # endregion

    # region Properties
    @property
    def ClassLevelCascadeMode(self) -> CascadeMode:
        return self._classLevelCascadeMode()

    @ClassLevelCascadeMode.setter
    def ClassLevelCascadeMode(self, value):
        self._classLevelCascadeMode = lambda: value

    @property
    def RuleLevelCascadeMode(self) -> CascadeMode:
        return self._ruleLevelCascadeMode()

    @RuleLevelCascadeMode.setter
    def RuleLevelCascadeMode(self, value):
        self._ruleLevelCascadeMode = lambda: value

    # endregion
