from __future__ import annotations
from typing import Callable, Optional, overload, override, TYPE_CHECKING
import asyncio

if TYPE_CHECKING:
    from src.fluent_validation.internal.ValidationStrategy import ValidationStrategy

from ..fluent_validation.IValidator import IValidator  # noqa: F401 We use it in the future
from .results.ValidationResult import ValidationResult
from .IValidationContext import IValidationContext, ValidationContext
from .syntax import IRuleBuilder
from .internal.PropertyRule import PropertyRule
from .internal.RuleBuilder import RuleBuilder
from .internal.RuleSetValidatorSelector import RulesetValidatorSelector

from .ValidatorOptions import ValidatorOptions
from .enums import CascadeMode


class AbstractValidator[T](IValidator[T]):
    # region constructor
    def __init__(self) -> None:
        self._classLevelCascadeMode: Callable[[], CascadeMode] = lambda: ValidatorOptions.Global.DefaultClassLevelCascadeMode
        self._ruleLevelCascadeMode: Callable[[], CascadeMode] = lambda: ValidatorOptions.Global.DefaultRuleLevelCascadeMode
        self._rules: list[PropertyRule] = []

    # endregion


    @overload
    def validate(self, instance: T) -> ValidationResult: ...

    @overload
    def validate(self, instance: IValidationContext) -> ValidationResult: ...

    @overload
    def validate(self, instance: T, options: Callable[[ValidationStrategy[T]], None]) -> ValidationResult: ...

    @override
    def validate(self, instance: T | IValidationContext, options: Optional[Callable[[ValidationStrategy[T]], None]] = None) -> ValidationResult:
        if options:
            return self.validate(ValidationContext[T].CreateWithOptions(instance, options))

        if not options and isinstance(instance,IValidationContext):
            # instance acts as context, due to does not exists override operator as C#, I need to call context attr as instance
            return self.__validate__(ValidationContext[T].GetFromNonGenericContext(instance))

        return self.__validate__(ValidationContext(instance, None, ValidatorOptions.Global.ValidatorSelectors.DefaultValidatorSelectorFactory()))

    def __validate__(self, context: ValidationContext[T]) -> ValidationResult:
        try:
            return asyncio.run(self.ValidateInternalAsync(context, False))
        except Exception:
            raise Exception

    async def ValidateInternalAsync(self, context: ValidationContext[T], useAsync: bool) -> ValidationResult:
        result: ValidationResult = ValidationResult(errors=context.Failures)

        count: int = len(self._rules)
        for i in range(count):
            await self._rules[i].ValidateAsync(context, useAsync)

            if self.ClassLevelCascadeMode == CascadeMode.Stop and len(result.errors) > 0:
                break

        self.SetExecutedRuleSets(result, context)

        # if (!result.IsValid && context.ThrowOnFailures) {
        #     RaiseValidationException(context, result);
        # }
        return result

        # COMMENT: used in private async ValueTask<ValidationResult> ValidateInternalAsync(ValidationContext<T> context, bool useAsync, CancellationToken cancellation) {...}

    def SetExecutedRuleSets(self, result: ValidationResult, context: ValidationContext[T]):
        obj = context.RootContextData.get("_FV_RuleSetsExecuted", None)
        if obj and isinstance(obj, set):
            result.RuleSetsExecuted = list(obj)
        else:
            result.RuleSetsExecuted = RulesetValidatorSelector.DefaultRuleSetNameInArray

    def rule_for[TProperty](self, func: Callable[[T], TProperty]) -> IRuleBuilder[T, TProperty]:  # IRuleBuilderInitial[T,TProperty]:
        rule: PropertyRule[T, TProperty] = PropertyRule.create(func, lambda: self.RuleLevelCascadeMode)
        self._rules.append(rule)
        return RuleBuilder[T, TProperty](rule, self)

    # FIXME [ ]: It's wrong implementation
    def rule_set(self, rule_set_name: str, action: Callable[..., None]) -> None:
        rule_set_names = [name.strip() for name in rule_set_name.split(",;")]
        setattr(self._rules, lambda r: setattr(r, "RuleSets", rule_set_names))
        return None

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
