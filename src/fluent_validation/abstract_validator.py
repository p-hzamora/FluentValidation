from __future__ import annotations
import threading
from typing import Any, Callable, Coroutine, Optional, Type, overload, override, TYPE_CHECKING
import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.fluent_validation.internal.ExtensionInternal import ExtensionsInternal

if TYPE_CHECKING:
    from src.fluent_validation.IValidationRuleInternal import IValidationRuleInternal
    from src.fluent_validation.internal.ValidationStrategy import ValidationStrategy
    from .syntax import IConditionBuilder, IRuleBuilder
    from src.fluent_validation.IValidationRule import IValidationRule

# from src.fluent_validation.internal.IncludeRule import IncludeRule
from src.fluent_validation.ValidationException import ValidationException
from src.fluent_validation.internal.ConditionBuilder import ConditionBuilder
from src.fluent_validation.AsyncValidatorInvokedSynchronouslyException import AsyncValidatorInvokedSynchronouslyException
from src.fluent_validation.internal.TrackingCollection import TrackingCollection
from src.fluent_validation.IValidator import IValidator  # noqa: F401 We use it in the future
from src.fluent_validation.results.ValidationResult import ValidationResult
from src.fluent_validation.IValidationContext import IValidationContext, ValidationContext
from src.fluent_validation.internal.PropertyRule import PropertyRule
from src.fluent_validation.internal.RuleBuilder import RuleBuilder
from src.fluent_validation.internal.RuleSetValidatorSelector import RulesetValidatorSelector

from src.fluent_validation.ValidatorOptions import ValidatorOptions
from src.fluent_validation.enums import CascadeMode


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
        # TODOH: It's not the correct way to control the nested event loop because in 'ChildValidatorAdaptor' class, when validating, context does not updated properly
        def run_coroutine_sync(coroutine: Coroutine[Any, Any, T], timeout: float = 30) -> T:
            def run_in_new_loop():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    return new_loop.run_until_complete(coroutine)
                finally:
                    new_loop.close()

            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                return asyncio.run(coroutine)

            if threading.current_thread() is threading.main_thread():
                if not loop.is_running():
                    return loop.run_until_complete(coroutine)
                else:
                    with ThreadPoolExecutor() as pool:
                        future = pool.submit(run_in_new_loop)
                        return future.result(timeout=timeout)
            else:
                return asyncio.run_coroutine_threadsafe(coroutine, loop).result()

        try:
            completedValueTask = self.ValidateInternalAsync(context, False)
            return run_coroutine_sync(completedValueTask)

        except RuntimeError:
            wasInvokeByMvc: bool = "InvokedByMvc" in context.RootContextData
            raise AsyncValidatorInvokedSynchronouslyException(type(self), wasInvokeByMvc)

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
        shouldContinue: bool = self.PreValidate(context, result)

        if not shouldContinue:
            if not result.is_valid and context.ThrowOnFailures:
                self.RaiseValidationException(context, result)

            return result

        count: int = len(self._rules)
        for i in range(count):
            totalFailures = len(context.Failures)
            await self._rules[i].ValidateAsync(context, useAsync)

            if self.ClassLevelCascadeMode == CascadeMode.Stop and len(result.errors) > totalFailures:
                break

        self.SetExecutedRuleSets(result, context)

        if not result.is_valid and context.ThrowOnFailures:
            self.RaiseValidationException(context, result)
        return result

        # COMMENT: used in private async ValueTask<ValidationResult> ValidateInternalAsync(ValidationContext<T> context, bool useAsync, CancellationToken cancellation) {...}

    def SetExecutedRuleSets(self, result: ValidationResult, context: ValidationContext[T]) -> None:
        obj = context.RootContextData.get("_FV_RuleSetsExecuted", None)
        if obj is not None and isinstance(obj, set):
            result.RuleSetsExecuted = list(obj)
        else:
            result.RuleSetsExecuted = RulesetValidatorSelector.DefaultRuleSetNameInArray
        return None

    # public virtual IValidatorDescriptor CreateDescriptor() => new ValidatorDescriptor<T>(Rules)

    def CanValidateInstancesOfType(self, _type: Type) -> bool:
        return issubclass(_type, self.__orig_bases__[0].__args__[0])

    def rule_for[TProperty](self, expression: Callable[[T], TProperty]) -> IRuleBuilder[T, TProperty]:  # IRuleBuilderInitial[T,TProperty]:
        ExtensionsInternal.Guard(expression,"Cannot pass null to RuleFor","expression")
        self._rules.append(rule)
        return RuleBuilder[T, TProperty](rule, self)

    #   public IRuleBuilderInitial<T, TTransformed> Transform<TProperty, TTransformed>(Expression<Func<T, TProperty>> from, Func<TProperty, TTransformed> to) {
    #         from.Guard("Cannot pass null to Transform", nameof(from))
    #         rule = PropertyRule<T, TTransformed>.Create(lambda: to,() => RuleLevelCascadeMode)
    #         Rules.Add(rule)
    #         OnRuleAdded(rule)
    #         return new RuleBuilder<T, TTransformed>(rule, this)
    #     }

    #     public IRuleBuilderInitial<T, TTransformed> Transform<TProperty, TTransformed>(Expression<Func<T, TProperty>> from, Func<T, TProperty, TTransformed> to) {
    #         from.Guard("Cannot pass null to Transform", nameof(from))
    #         rule = PropertyRule<T, TTransformed>.Create(lambda: to,() => RuleLevelCascadeMode)
    #         Rules.Add(rule)
    #         OnRuleAdded(rule)
    #         return new RuleBuilder<T, TTransformed>(rule, this)
    #     }

    #     public IRuleBuilderInitialCollection<T, TElement> RuleForEach<TElement>(Expression<Func<T, IEnumerable<TElement>>> expression) {
    #         expression.Guard("Cannot pass null to RuleForEach", nameof(expression))
    #         rule = CollectionPropertyRule<T, TElement>.Create(lambda: () > RuleLevelCascadeMode)
    #         Rules.Add(rule)
    #         OnRuleAdded(rule)
    #         return new RuleBuilder<T, TElement>(rule, this)
    #     }

    #     public IRuleBuilderInitialCollection<T, TTransformed> TransformForEach<TElement, TTransformed>(Expression<Func<T, IEnumerable<TElement>>> expression, Func<TElement, TTransformed> to) {
    #         expression.Guard("Cannot pass null to RuleForEach", nameof(expression))
    #         rule = CollectionPropertyRule<T, TTransformed>.CreateTransformed(lambda: to,() => RuleLevelCascadeMode)
    #         Rules.Add(rule)
    #         OnRuleAdded(rule)
    #         return new RuleBuilder<T, TTransformed>(rule, this)
    #     }

    #     public IRuleBuilderInitialCollection<T, TTransformed> TransformForEach<TElement, TTransformed>(Expression<Func<T, IEnumerable<TElement>>> expression, Func<T, TElement, TTransformed> to) {
    #         expression.Guard("Cannot pass null to RuleForEach", nameof(expression))
    #         rule = CollectionPropertyRule<T, TTransformed>.CreateTransformed(lambda: to,() => RuleLevelCascadeMode)
    #         Rules.Add(rule)
    #         OnRuleAdded(rule)
    #         return new RuleBuilder<T, TTransformed>(rule, this)
    #     }

    # FIXME [x]: It's wrong implementation
    def rule_set(self, rule_set_name: str, action: Callable[..., None]) -> None:
        rule_set_names = [name.strip() for name in rule_set_name.split(",")]
        with self._rules.OnItemAdded(lambda r: setattr(r, "RuleSets", rule_set_names)):
            action()
        return None

    @override
    def when(self, predicate: Callable[[T], bool], action: Callable[..., None]) -> IConditionBuilder:
        return self.__When(lambda x, _: predicate(x), action)

    def __When(self, predicate: Callable[[T, ValidationContext[T]], bool], action: Callable[..., None]) -> IConditionBuilder:
        return ConditionBuilder[T](self.Rules).when(predicate, action)

    @override
    def unless(self, predicate: Callable[[T], bool], action: Callable[..., None]) -> IConditionBuilder:
        return self.__Unless(lambda x, _: predicate(x), action)

    def __Unless(self, predicate: Callable[[T, ValidationContext[T]], bool], action: Callable[..., None]) -> IConditionBuilder:
        return ConditionBuilder[T](self.Rules).unless(predicate, action)

    # def WhenAsync(Func<T, CancellationToken, Task<bool>> predicate, Action action)->IConditionBuilder:
    #     return WhenAsync((x, _, cancel) => predicate(x, cancel), action)

    # def WhenAsync(Func<T, ValidationContext<T>, CancellationToken, Task<bool>> predicate, Action action)->IConditionBuilder:
    #     return new AsyncConditionBuilder<T>(Rules).WhenAsync(predicate, action)

    # def UnlessAsync(Func<T, CancellationToken, Task<bool>> predicate, Action action)->IConditionBuilder:
    #     return UnlessAsync((x, _, cancel) => predicate(x, cancel), action)

    # def UnlessAsync(Func<T, ValidationContext<T>, CancellationToken, Task<bool>> predicate, Action action)->IConditionBuilder:
    #     return new AsyncConditionBuilder<T>(Rules).UnlessAsync(predicate, action)

    # def Include(self, rulesToInclude:IValidator[T])->None:
    #     rule = IncludeRule[T].Create(rulesToInclude, lambda: self.RuleLevelCascadeMode)
    #     self.Rules.append(rule)
    #     self.OnRuleAdded(rule)

    # public void Include<TValidator>(Func<T, TValidator> rulesToInclude) where TValidator : IValidator[T] {
    #     rule = IncludeRule[T].Create(rulesToInclude, lambda: RuleLevelCascadeMode)
    #     Rules.Add(rule)
    #     OnRuleAdded(rule)
    # }

    # public IEnumerator<IValidationRule> GetEnumerator() => Rules.GetEnumerator()

    # IEnumerator IEnumerable.GetEnumerator() => GetEnumerator()

    def PreValidate(self, context: ValidationContext[T], result: ValidationResult) -> bool:
        return True

    def RaiseValidationException(self, context: ValidationContext[T], result: ValidationResult) -> None:
        raise ValidationException(errors=result.errors)

    def OnRuleAdded(rule: IValidationRule[T]) -> None:
        return None

    # region Properties
    @property
    def Rules(self) -> TrackingCollection[IValidationRuleInternal[T]]:
        return self._rules

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
