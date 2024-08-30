from __future__ import annotations

import inspect
from typing import Callable, TYPE_CHECKING, overload

from src.fluent_validation.enums import ApplyConditionTo, CascadeMode
from src.fluent_validation.IValidationContext import ValidationContext


if TYPE_CHECKING:
    from src.fluent_validation.syntax import (  # noqa: F401
        IRuleBuilderOptions,
        IRuleBuilderInitial,
        IRuleBuilder,
        IRuleBuilderInternal,
        IRuleBuilderOptionsConditions,
    )
    from .IValidationRule import IValidationRule


class DefaultValidatorOptions[T, TProperty]:
    @staticmethod
    def configurable(ruleBuilder: IRuleBuilder[T, TProperty]) -> IValidationRule[T, TProperty]:
        return ruleBuilder.Rule

    # def Configure(ruleBuilder:IRuleBuilderOptions[T, TProperty], configurator:Callable[[IValidationRule[T, TProperty]],None])->IRuleBuilderOptions[T, TProperty] :
    #     configurator(ruleBuilder.Configurable(ruleBuilder))
    #     return ruleBuilder

    # def Configure[T, TElement](this IRuleBuilderInitialCollection<T, TElement> ruleBuilder, Action<ICollectionRule<T, TElement>> configurator)->IRuleBuilderInitialCollection<T, TElement> :
    #     configurator(Configurable(ruleBuilder))
    #     return ruleBuilder

    # @staticmethod
    # def Configurable(ruleBuilder: IRuleBuilder[T, TProperty]) -> IValidationRule[T, TProperty]:
    #     return ruleBuilder.Rule

    # @staticmethod
    # def Configurable<T, TCollectionElement>(IRuleBuilderInitialCollection<T, TCollectionElement> ruleBuilder)->ICollectionRule<T, TCollectionElement> :
    #     return (ICollectionRule<T, TCollectionElement>) ((IRuleBuilderInternal<T, TCollectionElement>) ruleBuilder).Rule;

    # FIXME [ ]: the type of 'ruleBuilder' used to be 'IRuleBuilderInitial' and it should return the same
    def Cascade(ruleBuilder: IRuleBuilder[T, TProperty], cascadeMode: CascadeMode) -> IRuleBuilder[T, TProperty]:
        ruleBuilder.configurable(ruleBuilder).CascadeMode = cascadeMode
        return ruleBuilder

    # public static IRuleBuilderInitialCollection[T, TProperty] Cascade[T, TProperty](this IRuleBuilderInitialCollection[T, TProperty] ruleBuilder, CascadeMode cascadeMode) {
    #     Configurable(ruleBuilder).CascadeMode = cascadeMode;
    #     return ruleBuilder;
    # }

    @overload
    def with_message(ruleBuilder: IRuleBuilder[T, TProperty], errorMessage: str) -> IRuleBuilder[T, TProperty]: ...
    @overload
    def with_message(ruleBuilder: IRuleBuilder[T, TProperty], errorMessage: Callable[[T], str]) -> IRuleBuilder[T, TProperty]: ...
    @overload
    def with_message(ruleBuilder: IRuleBuilder[T, TProperty], errorMessage: Callable[[T, TProperty], str]) -> IRuleBuilder[T, TProperty]: ...

    def with_message(ruleBuilder: IRuleBuilder[T, TProperty], errorMessage: str | Callable[[T], str] | Callable[[T, TProperty], str]):
        if callable(errorMessage):
            n_params = len(inspect.signature(errorMessage).parameters)

            # TODOM: Check why 'instance_to_validate' is not detected by python's IDE
            if n_params == 1:
                ruleBuilder.configurable(ruleBuilder).Current.set_error_message(lambda ctx, _: errorMessage(None if ctx is not None else ctx.instance_to_validate))
            elif n_params == 2:
                ruleBuilder.configurable(ruleBuilder).Current.set_error_message(lambda ctx, value: errorMessage(None if ctx is not None else ctx.instance_to_validate, value))
        elif isinstance(errorMessage, str):
            DefaultValidatorOptions.configurable(ruleBuilder).Current.set_error_message(errorMessage)
        else:
            raise AttributeError

        return ruleBuilder

    # FIXME [ ]: the type of 'rule' used to be 'IRuleBuilderOptions' and it should return the same
    def WithErrorCode(rule: IRuleBuilder[T, TProperty], errorCode: str) -> IRuleBuilder[T, TProperty]:
        rule.configurable(rule).Current.ErrorCode = errorCode
        return rule

    # FIXME [ ]: the type of 'rule' used to be 'IRuleBuilderOptions' and it should return the same
    def when(rule: IRuleBuilder[T, TProperty], predicate: Callable[[T], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators) -> IRuleBuilder[T, TProperty]:
        return rule._When(lambda x, _: predicate(x), applyConditionTo)

    # def when(rule:IRuleBuilderOptionsConditions[T, TProperty], predicate:Callable[[T],bool], applyConditionTo:ApplyConditionTo = ApplyConditionTo.AllValidators)->IRuleBuilderOptionsConditions[T, TProperty]:
    #     return rule._When(lambda x, ctx: predicate(x), applyConditionTo)

    def _When(
        rule: IRuleBuilderOptions[T, TProperty],
        predicate: Callable[[T, ValidationContext[T]], bool],
        applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators,
    ) -> IRuleBuilderOptions[T, TProperty]:
        # Default behaviour for when/unless as of v1.3 is to apply the condition to all previous validators in the chain.
        rule.configurable(rule).ApplyCondition(lambda ctx: predicate(ctx.instance_to_validate, ValidationContext[T].GetFromNonGenericContext(ctx)), applyConditionTo)
        return rule

    # def when(rule:IRuleBuilderOptionsConditions[T, TProperty], predicate:Callable[[T, ValidationContext[T]], bool], applyConditionTo:ApplyConditionTo = ApplyConditionTo.AllValidators)->IRuleBuilderOptionsConditions[T, TProperty]:
    #     # Default behaviour for when/unless as of v1.3 is to apply the condition to all previous validators in the chain.
    #     rule.Configurable(rule).ApplyCondition(lambda ctx: predicate((T)ctx.InstanceToValidate, ValidationContext[T].GetFromNonGenericContext(ctx)), applyConditionTo)
    #     return rule

    # FIXME [ ]: the type of 'rule' used to be 'IRuleBuilderOptions' and it should return the same
    def unless(rule: IRuleBuilder[T, TProperty], predicate: Callable[[T], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators) -> IRuleBuilder[T, TProperty]:
        return rule._Unless(lambda x, _: predicate(x), applyConditionTo)

    # def unless(rule:IRuleBuilderOptionsConditions[T, TProperty], predicate:Callable[[T],bool], applyConditionTo:ApplyConditionTo = ApplyConditionTo.AllValidators)->IRuleBuilderOptionsConditions[T, TProperty]:
    #     return rule.unless(lambda x, ctx: predicate(x), applyConditionTo)

    # FIXME [ ]: the type of 'rule' used to be 'IRuleBuilder' and it should return the same
    def _Unless(
        rule: IRuleBuilder[T, TProperty], predicate: Callable[[T, ValidationContext[T]], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators
    ) -> IRuleBuilderOptions[T, TProperty]:
        return rule._When(lambda x, ctx: not predicate(x, ctx), applyConditionTo)

    # def unless(
    #     rule: IRuleBuilderOptionsConditions[T, TProperty], predicate: Callable[[T, ValidationContext[T]], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators
    # ) -> IRuleBuilderOptionsConditions[T, TProperty]:
    #     return rule.when(lambda x, ctx: not predicate(x, ctx), applyConditionTo)


#     public static IRuleBuilderOptions[T, TProperty] WhenAsync(rule:IRuleBuilderOptions[T, TProperty], Callable<T, CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
#         return rule.WhenAsync((x, ctx, ct) => predicate(x, ct), applyConditionTo);
#     }

#     public static IRuleBuilderOptionsConditions[T, TProperty] WhenAsync(rule:IRuleBuilderOptionsConditions[T, TProperty], Callable<T, CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
#         return rule.WhenAsync((x, ctx, ct) => predicate(x, ct), applyConditionTo);
#     }

#     public static IRuleBuilderOptions[T, TProperty] WhenAsync(rule:IRuleBuilderOptions[T, TProperty], Callable<T, ValidationContext[T], CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
#         # Default behaviour for when/unless as of v1.3 is to apply the condition to all previous validators in the chain.
#         Configurable(rule).ApplyAsyncCondition((ctx, ct) => predicate((T)ctx.InstanceToValidate, ValidationContext[T].GetFromNonGenericContext(ctx), ct), applyConditionTo);
#         return rule;
#     }

#     public static IRuleBuilderOptionsConditions[T, TProperty] WhenAsync(rule:IRuleBuilderOptionsConditions[T, TProperty], Callable<T, ValidationContext[T], CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
#         # Default behaviour for when/unless as of v1.3 is to apply the condition to all previous validators in the chain.
#         Configurable(rule).ApplyAsyncCondition((ctx, ct) => predicate((T)ctx.InstanceToValidate, ValidationContext[T].GetFromNonGenericContext(ctx), ct), applyConditionTo);
#         return rule;
#     }

#     public static IRuleBuilderOptions[T, TProperty] UnlessAsync(rule:IRuleBuilderOptions[T, TProperty], Callable<T, CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
#         return rule.UnlessAsync((x, ctx, ct) => predicate(x, ct), applyConditionTo);
#     }

#     public static IRuleBuilderOptionsConditions[T, TProperty] UnlessAsync(rule:IRuleBuilderOptionsConditions[T, TProperty], Callable<T, CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
#         return rule.UnlessAsync((x, ctx, ct) => predicate(x, ct), applyConditionTo);
#     }

#     public static IRuleBuilderOptions[T, TProperty] UnlessAsync(rule:IRuleBuilderOptions[T, TProperty], Callable<T, ValidationContext[T], CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
#         return rule.WhenAsync(async (x, ctx, ct) => !await predicate(x, ctx, ct), applyConditionTo);
#     }

#     public static IRuleBuilderOptionsConditions[T, TProperty] UnlessAsync(rule:IRuleBuilderOptionsConditions[T, TProperty], Callable<T, ValidationContext[T], CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
#         return rule.WhenAsync(async (x, ctx, ct) => !await predicate(x, ctx, ct), applyConditionTo);
#     }

#     public static IRuleBuilderInitialCollection<T, TCollectionElement> Where<T, TCollectionElement>(this IRuleBuilderInitialCollection<T, TCollectionElement> rule, Callable<TCollectionElement, bool> predicate) {
#         # This overload supports RuleFor().SetCollectionValidator() (which returns IRuleBuilderOptions<T, IEnumerable<TElement>>)
#         Configurable(rule).Filter = predicate;
#         return rule;
#     }

#     public static IRuleBuilderOptions[T, TProperty] WithName(rule:IRuleBuilderOptions[T, TProperty], str overridePropertyName) {
#         Configurable(rule).SetDisplayName(overridePropertyName);
#         return rule;
#     }

#     public static IRuleBuilderOptions[T, TProperty] WithName(rule:IRuleBuilderOptions[T, TProperty], Callable<T, str> nameProvider) {
#         # Must use null propagation here.
#         # The MVC clientside validation will try and retrieve the name, but won't
#         # be able to to so if we've used this overload of WithName.
#         Configurable(rule).SetDisplayName((context => {
#             T instance = context == null ? default : context.InstanceToValidate;
#             return nameProvider(instance);
#         }));
#         return rule;
#     }

#     public static IRuleBuilderOptions[T, TProperty] OverridePropertyName(rule:IRuleBuilderOptions[T, TProperty], str propertyName) {
#         # Allow str.Empty as this could be a model-level rule.
#         if (propertyName == null) throw new ArgumentNullException(nameof(propertyName), "A property name must be specified when calling OverridePropertyName.");
#         Configurable(rule).PropertyName = propertyName;
#         return rule;
#     }

#     public static IRuleBuilderOptions[T, TProperty] OverridePropertyName(rule:IRuleBuilderOptions[T, TProperty], Expression<Callable<T, object>> expr) {
#         if (expr == null) throw new ArgumentNullException(nameof(expr));
#         var member = expr.GetMember();
#         if (member == null) throw new NotSupportedException("Must supply a MemberExpression when calling OverridePropertyName");
#         return rule.OverridePropertyName(member.Name);
#     }

#     public static IRuleBuilderOptions[T, TProperty] WithState(rule:IRuleBuilderOptions[T, TProperty], Callable<T, object> stateProvider) {
#         var wrapper = new Callable<ValidationContext[T], TProperty, object>((ctx, _) => stateProvider(ctx.InstanceToValidate));
#         Configurable(rule).Current.CustomStateProvider = wrapper;
#         return rule;
#     }

#     public static IRuleBuilderOptions[T, TProperty] WithState(rule:IRuleBuilderOptions[T, TProperty], Callable<T, TProperty, object> stateProvider) {

#         var wrapper = new Callable<ValidationContext[T], TProperty, object>((ctx, val) => {
#             return stateProvider(ctx.InstanceToValidate, val);
#         });

#         Configurable(rule).Current.CustomStateProvider = wrapper;
#         return rule;
#     }

#     ///<summary>
#     public static IRuleBuilderOptions[T, TProperty] WithSeverity(rule:IRuleBuilderOptions[T, TProperty], Severity severity) {
#         Configurable(rule).Current.SeverityProvider = (_, _) => severity;
#         return rule;
#     }

#     public static IRuleBuilderOptions[T, TProperty] WithSeverity(rule:IRuleBuilderOptions[T, TProperty], Callable<T, Severity> severityProvider) {

#         Severity SeverityProvider(ValidationContext[T] ctx, TProperty value) {
#             return severityProvider(ctx.InstanceToValidate);
#         }

#         Configurable(rule).Current.SeverityProvider = SeverityProvider;
#         return rule;
#     }

#     public static IRuleBuilderOptions[T, TProperty] WithSeverity(rule:IRuleBuilderOptions[T, TProperty], Callable<T, TProperty, Severity> severityProvider) {

#         Severity SeverityProvider(ValidationContext[T] ctx, TProperty value) {
#             return severityProvider(ctx.InstanceToValidate, value);
#         }

#         Configurable(rule).Current.SeverityProvider = SeverityProvider;
#         return rule;
#     }

#     public static IRuleBuilderOptions[T, TProperty] WithSeverity(rule:IRuleBuilderOptions[T, TProperty], Callable<T, TProperty, ValidationContext[T], Severity> severityProvider) {

#         Severity SeverityProvider(ValidationContext[T] ctx, TProperty value) {
#             return severityProvider(ctx.InstanceToValidate, value, ctx);
#         }

#         Configurable(rule).Current.SeverityProvider = SeverityProvider;
#         return rule;
#     }

#     public static IRuleBuilderInitialCollection<T, TCollectionElement> OverrideIndexer<T, TCollectionElement>(this IRuleBuilderInitialCollection<T, TCollectionElement> rule, Callable<T, IEnumerable<TCollectionElement>, TCollectionElement, int, str> callback) {
#         # This overload supports RuleFor().SetCollectionValidator() (which returns IRuleBuilderOptions<T, IEnumerable<TElement>>)
#         Configurable(rule).IndexBuilder = callback;
#         return rule;
#     }
# }
