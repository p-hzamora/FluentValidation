from __future__ import annotations
import uuid
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from fluent_validation.IValidationContext import IValidationContext
    from fluent_validation.IValidationRuleInternal import IValidationRuleInternal
    from fluent_validation.internal.TrackingCollection import TrackingCollection

from fluent_validation.syntax import IConditionBuilder
from fluent_validation.IValidationContext import ValidationContext


class ConditionBuilder[T]:
    def __init__(self, rules: TrackingCollection[IValidationRuleInternal[T]]):
        self._rules: TrackingCollection[IValidationRuleInternal[T]] = rules

    def when(self, predicate: Callable[[T, ValidationContext[T]], bool], action: Callable[..., None]) -> IConditionBuilder:
        propertyRules: list[IValidationRuleInternal[T]] = []

        with self._rules.OnItemAdded(propertyRules.append):
            action()

        # Generate unique ID for this shared condition.
        id = "_FV_Condition_" + str(uuid.uuid4())

        def Condition(context: IValidationContext) -> bool:
            actualContext = ValidationContext[T].GetFromNonGenericContext(context)

            if actualContext.instance_to_validate is not None:
                if cachedResults := actualContext.SharedConditionCache.get(id, None):
                    if result := cachedResults.get(actualContext.instance_to_validate):
                        return result

            executionResult = predicate(actualContext.instance_to_validate, actualContext)
            if actualContext.instance_to_validate is not None:
                if cachedResults := actualContext.SharedConditionCache.get(id, None):
                    cachedResults[actualContext.instance_to_validate] = executionResult
                else:
                    actualContext.SharedConditionCache[id] = {actualContext.instance_to_validate: executionResult}
            return executionResult

        # Must apply the predicate after the rule has been fully created to ensure any rules-specific conditions have already been applied.
        for rule in propertyRules:
            rule.ApplySharedCondition(Condition)

        return ConditionOtherwiseBuilder[T](self._rules, Condition)

    def unless(self, predicate: Callable[[T, ValidationContext[T]], bool], action: Callable[..., None]) -> IConditionBuilder:
        return self.when(lambda x, context: not predicate(x, context), action)


# internal class AsyncConditionBuilder[T] {
# 	private TrackingCollection[IValidationRuleInternal[T]] _rules

# 	public AsyncConditionBuilder(TrackingCollection[IValidationRuleInternal[T]] rules) {
# 		_rules = rules
# 	}

# 	public IConditionBuilder WhenAsync(Func<T, ValidationContext[T], CancellationToken, Task<bool>> predicate, Action action) {
# 		propertyRules = new List[IValidationRuleInternal[T]]()

# 		using (_rules.OnItemAdded(propertyRules.Add)) {
# 			action()
# 		}

# 		// Generate unique ID for this shared condition.
# 		id = "_FV_AsyncCondition_" + Guid.NewGuid()

# 		async Task<bool> Condition(IValidationContext context, CancellationToken ct) {
# 			actualContext = ValidationContext[T].GetFromNonGenericContext(context)

# 			if (actualContext.instance_to_validate != null) {
# 				if (actualContext.SharedConditionCache.TryGetValue(id, out cachedResults)) {
# 					if (cachedResults.TryGetValue(actualContext.instance_to_validate, out bool result)) {
# 						return result
# 					}
# 				}
# 			}

# 			executionResult = await predicate((T)context.instance_to_validate, ValidationContext[T].GetFromNonGenericContext(context), ct)
# 			if (actualContext.instance_to_validate != null) {
# 				if (actualContext.SharedConditionCache.TryGetValue(id, out cachedResults)) {
# 					cachedResults.Add(actualContext.instance_to_validate, executionResult)
# 				}
# 				else {
# 					actualContext.SharedConditionCache.Add(id, new Dictionary<T, bool> {
# 						{ actualContext.instance_to_validate, executionResult }
# 					})
# 				}
# 			}
# 			return executionResult
# 		}

# 		foreach (rule in propertyRules) {
# 			rule.ApplySharedAsyncCondition(Condition)
# 		}

# 		return new AsyncConditionOtherwiseBuilder[T](_rules, Condition)
# 	}

# 	public IConditionBuilder UnlessAsync(Func<T, ValidationContext[T], CancellationToken, Task<bool>> predicate, Action action) {
# 		return WhenAsync(async (x, context, ct) => !await predicate(x, context, ct), action)
# 	}
# }


class ConditionOtherwiseBuilder[T](IConditionBuilder):
    def __init__(self, rules: TrackingCollection[IValidationRuleInternal[T]], condition: Callable[[IValidationContext], bool]):
        self._rules: TrackingCollection[IValidationRuleInternal[T]] = rules
        self._condition: Callable[[IValidationContext], bool] = condition

    def otherwise(self, action: Callable[..., None]) -> None:
        propertyRules: list[IValidationRuleInternal[T]] = []

        onRuleAdded: Callable[[IValidationRuleInternal[T]], None] = propertyRules.append

        with self._rules.OnItemAdded(onRuleAdded):
            action()

        for rule in propertyRules:
            rule.ApplySharedCondition(lambda ctx: not self._condition(ctx))


# internal class AsyncConditionOtherwiseBuilder[T] : IConditionBuilder {
# 	private TrackingCollection[IValidationRuleInternal[T]] _rules
# 	private readonly Func<IValidationContext, CancellationToken, Task<bool>> _condition

# 	public AsyncConditionOtherwiseBuilder(TrackingCollection[IValidationRuleInternal[T]] rules, Func<IValidationContext, CancellationToken, Task<bool>> condition) {
# 		_rules = rules
# 		_condition = condition
# 	}

# 	public virtual void otherwise(Action action) {
# 		propertyRules = new List[IValidationRuleInternal[T]]()

# 		Action[IValidationRuleInternal[T]] onRuleAdded = propertyRules.Add

# 		using (_rules.OnItemAdded(onRuleAdded)) {
# 			action()
# 		}

# 		foreach (rule in propertyRules) {
# 			rule.ApplySharedAsyncCondition(async (ctx, ct) => !await _condition(ctx, ct))
# 		}
# 	}
# }
