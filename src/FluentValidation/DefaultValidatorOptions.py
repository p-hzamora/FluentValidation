from typing import Callable  # noqa: F401
from .IValidationRule import IValidationRule
from .internal.RuleBuilder import RuleBuilder
from .syntax import IRuleBuilderInternal  # noqa: F401
from .syntax import IRuleBuilderOptions  # noqa: F401


class DefaultValidatorOptions:
    # IRuleBuilderInitial[T, TProperty> Configure[T, TProperty](this IRuleBuilderInitial[T, TProperty> ruleBuilder, Action[IValidationRule[T, TProperty]] configurator) {
    # 	configurator(Configurable(ruleBuilder))
    # 	return ruleBuilder
    # }

    # IRuleBuilderOptions[T, TProperty> Configure[T, TProperty](this IRuleBuilderOptions[T, TProperty> ruleBuilder, Action[IValidationRule[T, TProperty]] configurator) {
    # 	configurator(Configurable(ruleBuilder))
    # 	return ruleBuilder
    # }

    # IRuleBuilderInitialCollection[T, TElement> Configure[T, TElement](this IRuleBuilderInitialCollection[T, TElement> ruleBuilder, Action[ICollectionRule[T, TElement]] configurator) {
    # 	configurator(Configurable(ruleBuilder))
    # 	return ruleBuilder
    # }

    def Configurable[T, TProperty](ruleBuilder: RuleBuilder[T, TProperty]) -> IValidationRule[T, TProperty]:
        return ruleBuilder.Rule

    # def Configurable[T, TCollectionElement](ruleBuilder:IRuleBuilderInitialCollection[T, TCollectionElement])->ICollectionRule[T, TCollectionElement]:
    #     return(ICollectionRule[T, TCollectionElement]) ((IRuleBuilderInternal[T, TCollectionElement]) ruleBuilder).Rule


# IRuleBuilderInitial[T, TProperty> Cascade[T, TProperty](this IRuleBuilderInitial[T, TProperty> ruleBuilder, CascadeMode cascadeMode) {
# 	Configurable(ruleBuilder).CascadeMode = cascadeMode
# 	return ruleBuilder
# }

# IRuleBuilderInitialCollection[T, TProperty> Cascade[T, TProperty](this IRuleBuilderInitialCollection[T, TProperty> ruleBuilder, CascadeMode cascadeMode) {
# 	Configurable(ruleBuilder).CascadeMode = cascadeMode
# 	return ruleBuilder
# }

# IRuleBuilderOptions[T, TProperty> with_message[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, str errorMessage) {
# 	errorMessage.Guard("A message must be specified when calling with_message.", nameof(errorMessage))
# 	Configurable(rule).Current.SetErrorMessage(errorMessage)
# 	return rule
# }

# IRuleBuilderOptions[T, TProperty> with_message[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, str> messageProvider) {
# 	messageProvider.Guard("A messageProvider must be provided.", nameof(messageProvider))
# 	Configurable(rule).Current.SetErrorMessage((ctx, val) => {
# 		return messageProvider(ctx == null ? default : ctx.InstanceToValidate)
# 	})
# 	return rule
# }

# IRuleBuilderOptions[T, TProperty> with_message[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, TProperty, str> messageProvider) {
# 	messageProvider.Guard("A messageProvider must be provided.", nameof(messageProvider))
# 	Configurable(rule).Current.SetErrorMessage((context, value) => {
# 		return messageProvider(context == null ? default : context.InstanceToValidate, value)
# 	})
# 	return rule
# }

# IRuleBuilderOptions[T, TProperty> WithErrorCode[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, str errorCode) {
# 	errorCode.Guard("A error code must be specified when calling WithErrorCode.", nameof(errorCode))
# 	Configurable(rule).Current.ErrorCode = errorCode
# 	return rule
# }

# IRuleBuilderOptions[T, TProperty> When[T,TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, bool> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling When.", nameof(predicate))
# 	return rule.When((x, ctx) => predicate(x), applyConditionTo)
# }

# IRuleBuilderOptionsConditions[T, TProperty> When[T,TProperty](this IRuleBuilderOptionsConditions[T, TProperty> rule, Callable[T, bool> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling When.", nameof(predicate))
# 	return rule.When((x, ctx) => predicate(x), applyConditionTo)
# }

# IRuleBuilderOptions[T, TProperty> When[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, ValidationContext[T>, bool> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling When.", nameof(predicate))
# 	// Default behaviour for When/Unless as of v1.3 is to apply the condition to all previous validators in the chain.
# 	Configurable(rule).ApplyCondition(ctx => predicate((T)ctx.InstanceToValidate, ValidationContext[T].GetFromNonGenericContext(ctx)), applyConditionTo)
# 	return rule
# }

# IRuleBuilderOptionsConditions[T, TProperty> When[T, TProperty](this IRuleBuilderOptionsConditions[T, TProperty> rule, Callable[T, ValidationContext[T>, bool> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling When.", nameof(predicate))
# 	// Default behaviour for When/Unless as of v1.3 is to apply the condition to all previous validators in the chain.
# 	Configurable(rule).ApplyCondition(ctx => predicate((T)ctx.InstanceToValidate, ValidationContext[T].GetFromNonGenericContext(ctx)), applyConditionTo)
# 	return rule
# }

# IRuleBuilderOptions[T, TProperty> Unless[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, bool> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling Unless", nameof(predicate))
# 	return rule.Unless((x, ctx) => predicate(x), applyConditionTo)
# }

# IRuleBuilderOptionsConditions[T, TProperty> Unless[T, TProperty](this IRuleBuilderOptionsConditions[T, TProperty> rule, Callable[T, bool> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling Unless", nameof(predicate))
# 	return rule.Unless((x, ctx) => predicate(x), applyConditionTo)
# }

# IRuleBuilderOptions[T, TProperty> Unless[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, ValidationContext[T>, bool> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling Unless", nameof(predicate))
# 	return rule.When((x, ctx) => !predicate(x, ctx), applyConditionTo)
# }

# IRuleBuilderOptionsConditions[T, TProperty> Unless[T, TProperty](this IRuleBuilderOptionsConditions[T, TProperty> rule, Callable[T, ValidationContext[T>, bool> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling Unless", nameof(predicate))
# 	return rule.When((x, ctx) => !predicate(x, ctx), applyConditionTo)
# }

# IRuleBuilderOptions[T, TProperty> WhenAsync[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, CancellationToken, Task[bool]] predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling WhenAsync.", nameof(predicate))
# 	return rule.WhenAsync((x, ctx, ct) => predicate(x, ct), applyConditionTo)
# }

# IRuleBuilderOptionsConditions[T, TProperty> WhenAsync[T, TProperty](this IRuleBuilderOptionsConditions[T, TProperty> rule, Callable[T, CancellationToken, Task[bool]] predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling WhenAsync.", nameof(predicate))
# 	return rule.WhenAsync((x, ctx, ct) => predicate(x, ct), applyConditionTo)
# }

# IRuleBuilderOptions[T, TProperty> WhenAsync[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, ValidationContext[T>, CancellationToken, Task[bool]] predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling WhenAsync.", nameof(predicate))
# 	// Default behaviour for When/Unless as of v1.3 is to apply the condition to all previous validators in the chain.
# 	Configurable(rule).ApplyAsyncCondition((ctx, ct) => predicate((T)ctx.InstanceToValidate, ValidationContext[T].GetFromNonGenericContext(ctx), ct), applyConditionTo)
# 	return rule
# }

# IRuleBuilderOptionsConditions[T, TProperty> WhenAsync[T, TProperty](this IRuleBuilderOptionsConditions[T, TProperty> rule, Callable[T, ValidationContext[T>, CancellationToken, Task[bool]] predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling WhenAsync.", nameof(predicate))
# 	// Default behaviour for When/Unless as of v1.3 is to apply the condition to all previous validators in the chain.
# 	Configurable(rule).ApplyAsyncCondition((ctx, ct) => predicate((T)ctx.InstanceToValidate, ValidationContext[T].GetFromNonGenericContext(ctx), ct), applyConditionTo)
# 	return rule
# }

# IRuleBuilderOptions[T, TProperty> UnlessAsync[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, CancellationToken, Task[bool]] predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling UnlessAsync", nameof(predicate))
# 	return rule.UnlessAsync((x, ctx, ct) => predicate(x, ct), applyConditionTo)
# }

# IRuleBuilderOptionsConditions[T, TProperty> UnlessAsync[T, TProperty](this IRuleBuilderOptionsConditions[T, TProperty> rule, Callable[T, CancellationToken, Task[bool]] predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling UnlessAsync", nameof(predicate))
# 	return rule.UnlessAsync((x, ctx, ct) => predicate(x, ct), applyConditionTo)
# }

# IRuleBuilderOptions[T, TProperty> UnlessAsync[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, ValidationContext[T>, CancellationToken, Task[bool]] predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling UnlessAsync", nameof(predicate))
# 	return rule.WhenAsync(async (x, ctx, ct) => !await predicate(x, ctx, ct), applyConditionTo)
# }

# IRuleBuilderOptionsConditions[T, TProperty> UnlessAsync[T, TProperty](this IRuleBuilderOptionsConditions[T, TProperty> rule, Callable[T, ValidationContext[T>, CancellationToken, Task[bool]] predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
# 	predicate.Guard("A predicate must be specified when calling UnlessAsync", nameof(predicate))
# 	return rule.WhenAsync(async (x, ctx, ct) => !await predicate(x, ctx, ct), applyConditionTo)
# }

# IRuleBuilderInitialCollection[T, TCollectionElement> Where[T, TCollectionElement](this IRuleBuilderInitialCollection[T, TCollectionElement> rule, Callable[TCollectionElement, bool> predicate) {
# 	// This overload supports rule_for().SetCollectionValidator() (which returns IRuleBuilderOptions[T, IEnumerable[TElement]])
# 	predicate.Guard("Cannot pass null to Where.", nameof(predicate))
# 	Configurable(rule).Filter = predicate
# 	return rule
# }

# @classmethod
# def WithName[T, TProperty](cls,rule:IRuleBuilderOptions[T, TProperty], overridePropertyName:str)->IRuleBuilderOptions[T, TProperty]:
#     overridePropertyName.Guard("A property name must be specified when calling WithName.", nameof(overridePropertyName))
#     cls.Configurable(rule).SetDisplayName(overridePropertyName)
#     return rule

# @classmethod
# def WithName[T, TProperty](cls, rule:IRuleBuilderOptions[T, TProperty], nameProvider:Callable[[T], str])->IRuleBuilderOptions[T, TProperty]:
#     nameProvider.Guard("A nameProvider WithName.", nameof(nameProvider))
#     # must use null propagation here.
#     # The MVC clientside validation will try and retrieve the name, but won't
#     # be able to to so if we've used this overload of WithName.
#     cls.Configurable(rule).SetDisplayName((context => {
#         T instance = context == null ? default : context.InstanceToValidate
#         return nameProvider(instance)
#     }))
#     return rule

# IRuleBuilderOptions[T, TProperty> OverridePropertyName[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, str propertyName) {
# 	// Allow str.Empty as this could be a model-level rule.
# 	if (propertyName == null) throw new ArgumentNullException(nameof(propertyName), "A property name must be specified when calling OverridePropertyName.")
# 	Configurable(rule).PropertyName = propertyName
# 	return rule
# }

# IRuleBuilderOptions[T, TProperty> OverridePropertyName[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Expression[Callable[T, object]] expr) {
# 	if (expr == null) throw new ArgumentNullException(nameof(expr))
# 	var member = expr.GetMember()
# 	if (member == null) throw new NotSupportedException("must supply a MemberExpression when calling OverridePropertyName")
# 	return rule.OverridePropertyName(member.Name)
# }

# IRuleBuilderOptions[T, TProperty> WithState[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, object> stateProvider) {
# 	stateProvider.Guard("A lambda expression must be passed to WithState", nameof(stateProvider))
# 	var wrapper = new Callable[ValidationContext[T>, TProperty, object]((ctx, _) => stateProvider(ctx.InstanceToValidate))
# 	Configurable(rule).Current.CustomStateProvider = wrapper
# 	return rule
# }

# IRuleBuilderOptions[T, TProperty> WithState[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, TProperty, object> stateProvider) {
# 	stateProvider.Guard("A lambda expression must be passed to WithState", nameof(stateProvider))

# 	var wrapper = new Callable[ValidationContext[T>, TProperty, object]((ctx, val) => {
# 		return stateProvider(ctx.InstanceToValidate, val)
# 	})

# 	Configurable(rule).Current.CustomStateProvider = wrapper
# 	return rule
# }

# IRuleBuilderOptions[T, TProperty> WithSeverity[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Severity severity) {
# 	Configurable(rule).Current.SeverityProvider = (_, _) => severity
# 	return rule
# }

# IRuleBuilderOptions[T, TProperty> WithSeverity[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, Severity> severityProvider) {
# 	severityProvider.Guard("A lambda expression must be passed to WithSeverity", nameof(severityProvider))

# 	Severity SeverityProvider(ValidationContext[T> ctx, TProperty value) {
# 		return severityProvider(ctx.InstanceToValidate)
# 	}

# 	Configurable(rule).Current.SeverityProvider = SeverityProvider
# 	return rule
# }

# IRuleBuilderOptions[T, TProperty> WithSeverity[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, TProperty, Severity> severityProvider) {
# 	severityProvider.Guard("A lambda expression must be passed to WithSeverity", nameof(severityProvider))

# 	Severity SeverityProvider(ValidationContext[T> ctx, TProperty value) {
# 		return severityProvider(ctx.InstanceToValidate, value)
# 	}

# 	Configurable(rule).Current.SeverityProvider = SeverityProvider
# 	return rule
# }

# IRuleBuilderOptions[T, TProperty> WithSeverity[T, TProperty](this IRuleBuilderOptions[T, TProperty> rule, Callable[T, TProperty, ValidationContext[T>, Severity> severityProvider) {
# 	severityProvider.Guard("A lambda expression must be passed to WithSeverity", nameof(severityProvider))

# 	Severity SeverityProvider(ValidationContext[T> ctx, TProperty value) {
# 		return severityProvider(ctx.InstanceToValidate, value, ctx)
# 	}

# 	Configurable(rule).Current.SeverityProvider = SeverityProvider
# 	return rule
# }

# IRuleBuilderInitialCollection[T, TCollectionElement> OverrideIndexer[T, TCollectionElement](this IRuleBuilderInitialCollection[T, TCollectionElement> rule, Callable[T, IEnumerable[TCollectionElement>, TCollectionElement, int, str> callback) {
# 	// This overload supports rule_for().SetCollectionValidator() (which returns IRuleBuilderOptions[T, IEnumerable[TElement]])
# 	callback.Guard("Cannot pass null to OverrideIndexer.", nameof(callback))
# 	Configurable(rule).IndexBuilder = callback
# 	return rule
# }
