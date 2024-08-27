from __future__ import annotations
from typing import Callable, Optional, overload, override, TYPE_CHECKING
import asyncio

if TYPE_CHECKING:
    from src.fluent_validation.IValidationRuleInternal import IValidationRuleInternal
    from src.fluent_validation.internal.ValidationStrategy import ValidationStrategy

from src.fluent_validation.AsyncValidatorInvokedSynchronouslyException import AsyncValidatorInvokedSynchronouslyException
from src.fluent_validation.internal.TrackingCollection import TrackingCollection
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
        self._rules: TrackingCollection[IValidationRuleInternal] = TrackingCollection()

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

        if not options and isinstance(instance, IValidationContext):
            # instance acts as context, due to does not exists override operator as C#, I need to call context attr as instance
            return self.__validate__(ValidationContext[T].GetFromNonGenericContext(instance))

        if not options and type(instance) is ValidationContext:
            return self.__validate__(instance)

        return self.__validate__(ValidationContext[T](instance, None, ValidatorOptions.Global.ValidatorSelectors.DefaultValidatorSelectorFactory()))

    def __validate__(self, context: ValidationContext[T]) -> ValidationResult:
    @overload
    async def ValidateAsync(self, instance: IValidationContext) -> ValidationResult: ...
    @overload
    async def ValidateAsync(self, instance: T) -> ValidationResult: ...

    @override
    async def ValidateAsync(self, instance):
        if isinstance(instance, IValidationContext):
            return await self.__validate_async__(ValidationContext[T].GetFromNonGenericContext(instance))

        return await self.__validate_async__(ValidationContext[T](instance, None, ValidatorOptions.Global.ValidatorSelectors.DefaultValidatorSelectorFactory()))

    async def __validate_async__(self, instance: ValidationContext[T]):
        instance.IsAsync = True
        return await self.ValidateInternalAsync(instance, useAsync=True)

    async def ValidateInternalAsync(self, context: ValidationContext[T], useAsync: bool) -> ValidationResult:
        result: ValidationResult = ValidationResult(errors=context.Failures)

        count: int = len(self._rules)
        for i in range(count):
            totalFailures = len(context.Failures)
            await self._rules[i].ValidateAsync(context, useAsync)

            if self.ClassLevelCascadeMode == CascadeMode.Stop and len(result.errors) > totalFailures:
                break

        self.SetExecutedRuleSets(result, context)

        # if (!result.IsValid && context.ThrowOnFailures) {
        #     RaiseValidationException(context, result);
        # }
        return result

        # COMMENT: used in private async ValueTask<ValidationResult> ValidateInternalAsync(ValidationContext<T> context, bool useAsync, CancellationToken cancellation) {...}

    def SetExecutedRuleSets(self, result: ValidationResult, context: ValidationContext[T]) -> None:
        obj = context.RootContextData.get("_FV_RuleSetsExecuted", None)
        if obj is not None and isinstance(obj, set):
            result.RuleSetsExecuted = list(obj)
        else:
            result.RuleSetsExecuted = RulesetValidatorSelector.DefaultRuleSetNameInArray
        return None

    # public virtual IValidatorDescriptor CreateDescriptor() => new ValidatorDescriptor<T>(Rules);

    def CanValidateInstancesOfType(self, _type: Type) -> bool:
        return issubclass(_type, self.__orig_bases__[0].__args__[0])

    def rule_for[TProperty](self, func: Callable[[T], TProperty]) -> IRuleBuilder[T, TProperty]:  # IRuleBuilderInitial[T,TProperty]:
        rule: PropertyRule[T, TProperty] = PropertyRule.create(func, lambda: self.RuleLevelCascadeMode)
        self._rules.append(rule)
        return RuleBuilder[T, TProperty](rule, self)

    #   public IRuleBuilderInitial<T, TTransformed> Transform<TProperty, TTransformed>(Expression<Func<T, TProperty>> from, Func<TProperty, TTransformed> to) {
    #         from.Guard("Cannot pass null to Transform", nameof(from));
    #         var rule = PropertyRule<T, TTransformed>.Create(from, to, () => RuleLevelCascadeMode);
    #         Rules.Add(rule);
    #         OnRuleAdded(rule);
    #         return new RuleBuilder<T, TTransformed>(rule, this);
    #     }

    #     public IRuleBuilderInitial<T, TTransformed> Transform<TProperty, TTransformed>(Expression<Func<T, TProperty>> from, Func<T, TProperty, TTransformed> to) {
    #         from.Guard("Cannot pass null to Transform", nameof(from));
    #         var rule = PropertyRule<T, TTransformed>.Create(from, to, () => RuleLevelCascadeMode);
    #         Rules.Add(rule);
    #         OnRuleAdded(rule);
    #         return new RuleBuilder<T, TTransformed>(rule, this);
    #     }

    #     public IRuleBuilderInitialCollection<T, TElement> RuleForEach<TElement>(Expression<Func<T, IEnumerable<TElement>>> expression) {
    #         expression.Guard("Cannot pass null to RuleForEach", nameof(expression));
    #         var rule = CollectionPropertyRule<T, TElement>.Create(expression, () => RuleLevelCascadeMode);
    #         Rules.Add(rule);
    #         OnRuleAdded(rule);
    #         return new RuleBuilder<T, TElement>(rule, this);
    #     }

    #     public IRuleBuilderInitialCollection<T, TTransformed> TransformForEach<TElement, TTransformed>(Expression<Func<T, IEnumerable<TElement>>> expression, Func<TElement, TTransformed> to) {
    #         expression.Guard("Cannot pass null to RuleForEach", nameof(expression));
    #         var rule = CollectionPropertyRule<T, TTransformed>.CreateTransformed(expression, to, () => RuleLevelCascadeMode);
    #         Rules.Add(rule);
    #         OnRuleAdded(rule);
    #         return new RuleBuilder<T, TTransformed>(rule, this);
    #     }

    #     public IRuleBuilderInitialCollection<T, TTransformed> TransformForEach<TElement, TTransformed>(Expression<Func<T, IEnumerable<TElement>>> expression, Func<T, TElement, TTransformed> to) {
    #         expression.Guard("Cannot pass null to RuleForEach", nameof(expression));
    #         var rule = CollectionPropertyRule<T, TTransformed>.CreateTransformed(expression, to, () => RuleLevelCascadeMode);
    #         Rules.Add(rule);
    #         OnRuleAdded(rule);
    #         return new RuleBuilder<T, TTransformed>(rule, this);
    #     }

    # FIXME [x]: It's wrong implementation
    def rule_set(self, rule_set_name: str, action: Callable[..., None]) -> None:
        rule_set_names = [name.strip() for name in rule_set_name.split(",")]
        with self._rules.OnItemAdded(lambda r: setattr(r, "RuleSets", rule_set_names)):
            action()
        return None

    # public IConditionBuilder When(Func<T, bool> predicate, Action action)
    #     => When((x, _) => predicate(x), action);

    # public IConditionBuilder When(Func<T, ValidationContext<T>, bool> predicate, Action action)
    #     => new ConditionBuilder<T>(Rules).When(predicate, action);

    # public IConditionBuilder Unless(Func<T, bool> predicate, Action action)
    #     => Unless((x, _) => predicate(x), action);

    # public IConditionBuilder Unless(Func<T, ValidationContext<T>, bool> predicate, Action action)
    #     => new ConditionBuilder<T>(Rules).Unless(predicate, action);

    # public IConditionBuilder WhenAsync(Func<T, CancellationToken, Task<bool>> predicate, Action action)
    #     => WhenAsync((x, _, cancel) => predicate(x, cancel), action);

    # public IConditionBuilder WhenAsync(Func<T, ValidationContext<T>, CancellationToken, Task<bool>> predicate, Action action)
    #     => new AsyncConditionBuilder<T>(Rules).WhenAsync(predicate, action);

    # public IConditionBuilder UnlessAsync(Func<T, CancellationToken, Task<bool>> predicate, Action action)
    #     => UnlessAsync((x, _, cancel) => predicate(x, cancel), action);

    # public IConditionBuilder UnlessAsync(Func<T, ValidationContext<T>, CancellationToken, Task<bool>> predicate, Action action)
    #     => new AsyncConditionBuilder<T>(Rules).UnlessAsync(predicate, action);

    # public void Include(IValidator<T> rulesToInclude) {
    #     rulesToInclude.Guard("Cannot pass null to Include", nameof(rulesToInclude));
    #     var rule = IncludeRule<T>.Create(rulesToInclude, () => RuleLevelCascadeMode);
    #     Rules.Add(rule);
    #     OnRuleAdded(rule);
    # }

    # public void Include<TValidator>(Func<T, TValidator> rulesToInclude) where TValidator : IValidator<T> {
    #     rulesToInclude.Guard("Cannot pass null to Include", nameof(rulesToInclude));
    #     var rule = IncludeRule<T>.Create(rulesToInclude, () => RuleLevelCascadeMode);
    #     Rules.Add(rule);
    #     OnRuleAdded(rule);
    # }

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
