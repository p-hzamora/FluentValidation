from __future__ import annotations
from typing import Any, Callable, Type, TYPE_CHECKING
from fluent_validation.AsyncValidatorInvokedSynchronouslyException import AsyncValidatorInvokedSynchronouslyException
from fluent_validation.ICollectionRule import ICollectionRule
from fluent_validation.IValidationRuleInternal import IValidationRuleInternal
from fluent_validation.MemberInfo import MemberInfo
from fluent_validation.enums import CascadeMode
from fluent_validation.internal.AccessorCache import AccessorCache
from fluent_validation.internal.RuleBase import RuleBase
from fluent_validation.internal.RuleComponent import RuleComponent
from fluent_validation.LambdaExpression import LambdaExpression


if TYPE_CHECKING:
    from fluent_validation.IValidationContext import ValidationContext


class CollectionPropertyRule[T, TElement](RuleBase[T, list[TElement], TElement], ICollectionRule[T, TElement], IValidationRuleInternal[T, TElement]):
    def __init__(self, member: MemberInfo, propertyFunc: Callable[[T], list[TElement]], expression: Callable[..., Any], cascadeModeThunk: Callable[[], CascadeMode], typeToValidate: Type):
        """
        Initializes new instance of the CollectionPropertyRule class
        """
        super().__init__(member, propertyFunc, expression, cascadeModeThunk, typeToValidate)
        self._Filter: Callable[[TElement], bool] = None
        self._IndexBuilder: Callable[[T, list[TElement], TElement, int], str] = None

    @property
    def Filter(self) -> Callable[[TElement], bool]:
        """
        Filter that should include/exclude items in the collection.
        """
        return self._Filter

    @Filter.setter
    def Filter(self, value: Callable[[TElement], bool]) -> None:
        self._Filter = value

    @property
    def IndexBuilder(self) -> Callable[[T, list[TElement], TElement, int], str]:
        """
        Constructs the indexer in the property name associated with the error message.
        By default this is "[" + index + "]"
        """
        return self._IndexBuilder

    @IndexBuilder.setter
    def IndexBuilder(self, value: Callable[[T, list[TElement], TElement, int], str]) -> None:
        self._IndexBuilder = value

    @classmethod
    def Create(cls, expression: Callable[[T], list[TElement]], cascadeModeThunk: Callable[[], CascadeMode], bypassCache: bool = False) -> CollectionPropertyRule[T, TElement]:
        """
        Creates a new property rule from a lambda expression.
        """
        # FIXME [ ]: test_Uses_useful_error_message_when_used_on_non_property fails due to  MemberInfo() should return None instead any valu
        member = MemberInfo(expression)
        compiled = AccessorCache[T].GetCachedAccessor(member, expression, bypassCache, "FV_RuleForEach")
        return CollectionPropertyRule[T, TElement](member, lambda x: compiled(x), expression, cascadeModeThunk, type(TElement))

    # 	internal static CollectionPropertyRule[T, TElement] CreateTransformed<TOriginal>(Expression<Func<T, list<TOriginal>>> expression, Func<TOriginal, TElement> transformer, Func<CascadeMode> cascadeModeThunk, bool bypassCache = False) {
    # 		"""
    # 		Creates a new property rule from a lambda expression.
    # 		"""
    # 		member = expression.GetMember()
    # 		compiled = AccessorCache[T].GetCachedAccessor(member, expression, bypassCache, "FV_RuleForEach")

    # 		list<TElement> PropertyFunc(T instance) =>
    # 			compiled(instance).Select(transformer)

    # 		return new CollectionPropertyRule[T, TElement](member, PropertyFunc, expression, cascadeModeThunk, type(TElement))
    # 	}

    # 	internal static CollectionPropertyRule[T, TElement] CreateTransformed<TOriginal>(Expression<Func<T, list<TOriginal>>> expression, Func<T, TOriginal, TElement> transformer, Func<CascadeMode> cascadeModeThunk, bool bypassCache = False) {
    # 		"""
    # 		Creates a new property rule from a lambda expression.
    # 		"""
    # 		member = expression.GetMember()
    # 		compiled = AccessorCache[T].GetCachedAccessor(member, expression, bypassCache, "FV_RuleForEach")

    # 		list<TElement> PropertyFunc(T instance) {
    # 			return compiled(instance).Select(element => transformer(instance, element))
    # 		}

    # 		return new CollectionPropertyRule[T, TElement](member, PropertyFunc, expression, cascadeModeThunk, type(TOriginal))
    # 	}

    async def ValidateAsync(self, context: ValidationContext[T], useAsync: bool):  # CancellationToken cancellation
        async def AfterValidate():
            if len(context.Failures) <= totalFailures and self.DependentRules is not None:
                for dependentRule in self.DependentRules:
                    # cancellation.ThrowIfCancellationRequested()
                    await dependentRule.ValidateAsync(context, useAsync)  # , cancellation
            return None

        displayName: None | str = self.get_display_name(context)

        if self.PropertyName is None and displayName is None:
            # No name has been specified. Assume this is a model-level rule, so we should use empty str instead.
            displayName = ""

        # Construct the full name of the property, taking into account overriden property names and the chain (if we're in a nested validator)
        propertyName: str = context.PropertyChain.BuildPropertyPath(displayName if not self.PropertyName else self.PropertyName)

        if propertyName is None or propertyName == "":
            propertyName = self.InferPropertyName(self.Expression)

        # Ensure that this rule is allowed to run.
        # The validatselector has the opportunity to veto this before any of the validators execute.
        if not context.Selector.CanExecute(self, propertyName, context):
            return None

        if self.Condition:
            if not self.Condition(context):
                return None

        # if (AsyncCondition is not None) {
        # 	if (useAsync) {
        # 		if (!await AsyncCondition(context, cancellation)) {
        # 			return
        # 		}
        # 	}
        # 	else {
        # 		throw new AsyncValidatorInvokedSynchronouslyException()
        # 	}
        # }

        filteredValidators = await self.GetValidatorsToExecuteAsync(context, useAsync)

        if len(filteredValidators) == 0:
            # If there are no property validators to execute after running the conditions, bail out.
            return None

        cascade = self.CascadeMode

        try:
            # FIXME [x]: Get the error most similar to 'NullReferenceException'
            collection: list[TElement] = self.PropertyFunc(context.instance_to_validate)
        except TypeError:
            raise TypeError(f"TypeError occurred when executing rule for '{self.Expression.lambda_to_string}'. If this property can be None you should add a null check using a when condition")
        count: int = 0
        totalFailures: int = len(context.Failures)

        if collection is not None:
            if propertyName is None or propertyName == "":
                raise RuntimeError("Could not automatically determine the property name ")

            for element in collection:
                index: int = count
                count += 1

                if self.Filter is not None and not self.Filter(element):
                    continue

                indexer: str = str(index)
                useDefaultIndexFormat: bool = True

                if self.IndexBuilder is not None:
                    indexer = self.IndexBuilder(context.instance_to_validate, collection, element, index)
                    useDefaultIndexFormat = False

                context.PrepareForChildCollectionValidator()
                context.PropertyChain.Add(propertyName)
                context.PropertyChain.AddIndexer(indexer, useDefaultIndexFormat)

                valueToValidate = element
                propertyPath = context.PropertyChain.ToString()
                totalFailuresInner = len(context.Failures)
                context.InitializeForPropertyValidator(propertyPath, self._displayNameFunc, self.PropertyName)

                for component in filteredValidators:
                    context.MessageFormatter.Reset()
                    context.MessageFormatter.AppendArgument("CollectionIndex", index)

                    valid: bool = await component.ValidateAsync(context, valueToValidate, useAsync)  # , cancellation

                    if not valid:
                        self.PrepareMessageFormatterForValidationError(context, valueToValidate)
                        failure = self.CreateValidationError(context, valueToValidate, component)
                        context.Failures.append(failure)

                    # If there has been at least one failure, and our CascadeMode has been set to Stop
                    # then don't continue to the next rule
                    if len(context.Failures) > totalFailuresInner and cascade == CascadeMode.Stop:
                        context.RestoreState()
                        return await AfterValidate()  # 🙃
                context.RestoreState()
        return await AfterValidate()

    def AddDependentRules(self, rules: list[IValidationRuleInternal[T]]) -> None:
        # TODOM: Checked if the translation is correct
        if self.DependentRules is None:
            self.DependentRules = []
        self.DependentRules.extend(rules)

    async def GetValidatorsToExecuteAsync(self, context: ValidationContext[T], useAsync: bool) -> list[RuleComponent[T, TElement]]:
        # Loop over each validator and check if its condition allows it to run.
        # This needs to be done prior to the main loop as within a collection rule
        # validators' conditions still act upon the root object, not upon the collection property.
        # This allows the property validators to cancel their execution prior to the collection
        # being retrieved (thereby possibly avoiding NullReferenceExceptions).
        # Must call ToList (copy in Python) so we don't modify the original collection mid-loop.
        validators = self.Components.copy()

        for component in self.Components:
            if component.HasCondition:
                if not component.InvokeCondition(context):
                    validators.remove(component)

            if component.HasAsyncCondition:
                if useAsync:
                    if not await component.InvokeAsyncCondition(context):
                        validators.remove(component)
                else:
                    raise AsyncValidatorInvokedSynchronouslyException()

        return validators

    @staticmethod
    def InferPropertyName(expression: LambdaExpression) -> str:
        # TODOM: Checked
        paramExp = expression.lambda_to_string

        if paramExp is None:
            raise ValueError(
                "Could not infer property name for expression: "
                + expression
                + '. Please explicitly specify a property name by calling orverride_property_name as part of the rule chain. Eg: rule_for_each(lambda x: x).NotNull().orverride_property_name("MyProperty")'
            )

        return paramExp
