from __future__ import annotations
from typing import Any, Callable, Type, Optional, TYPE_CHECKING, overload

from fluent_validation.MemberInfo import MemberInfo
from fluent_validation.ValidatorOptions import ValidatorOptions
from fluent_validation.internal.ExtensionInternal import ExtensionsInternal
from fluent_validation.IValidationRule import IValidationRule
from fluent_validation.internal.IRuleComponent import IRuleComponent
from fluent_validation.internal.MessageBuilderContext import IMessageBuilderContext, MessageBuilderContext
from fluent_validation.internal.RuleComponent import RuleComponent
from fluent_validation.results.ValidationFailure import ValidationFailure


from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.enums import ApplyConditionTo, CascadeMode
from fluent_validation.LambdaExpression import LambdaExpression

if TYPE_CHECKING:
    from fluent_validation.IValidationRuleInternal import IValidationRuleInternal
    from fluent_validation.validators.IpropertyValidator import IAsyncPropertyValidator, IPropertyValidator


class RuleBase[T, TProperty, TValue](IValidationRule[T, TValue]):
    def __init__(
        self,
        member: MemberInfo,
        propertyFunc: Callable[[T], TProperty],
        expression: Callable[..., Any],
        cascadeModeThunk: Callable[[], CascadeMode],
        typeToValidate: Type,
    ):
        self._member: MemberInfo = member if member is not None else MemberInfo(lambda: None)
        self._PropertyFunc = propertyFunc
        self._expression: Callable[..., Any] = expression
        self._typeToValidate: Type = typeToValidate
        self._cascadeModeThunk: Callable[[], CascadeMode] = cascadeModeThunk

        containerType = type(T)
        self._propertyDisplayName: Optional[str] = None
        self.PropertyName: Optional[str] = ValidatorOptions.Global.PropertyNameResolver(containerType, self._member, expression)
        self._displayNameFactory: Callable[[ValidationContext[T], str]] = lambda context: ValidatorOptions.Global.DisplayNameResolver(containerType, self._member, expression)

        self._displayNameFunc: Callable[[ValidationContext[T], str]] = self.get_display_name

        self._components: list[RuleComponent[T, TProperty]] = []
        self._condition: Optional[Callable[[ValidationContext[T]], bool]] = None

        self._displayName: str = None
        self._rule_sets: Optional[list[str]] = None
        self._DependentRules: list[IValidationRuleInternal[T]] = None
        self._MessageBuilder:None| Callable[[IMessageBuilderContext[T, TProperty]], str] = None

    def AddValidator(self, validator: IPropertyValidator[T, TValue]) -> None:
        component = RuleComponent[T, TValue](validator)
        self._components.append(component)

    def AddAsyncValidator(self, asyncValidator: IAsyncPropertyValidator[T, TValue], fallback: IPropertyValidator[T, TValue] = None) -> None:
        component = RuleComponent[T, TValue](asyncValidator, fallback)
        self._components.append(component)

    def ClearValidators(self) -> None:
        self._components.clear()

    def get_display_name(self, context: ValidationContext[T]) -> None | str:
        if self._displayNameFactory is not None and (res := self._displayNameFactory(context)) is not None:
            return res
        elif self._displayName is not None:
            return self._displayName
        else:
            return self._propertyDisplayName

    @property
    def Member(self) -> MemberInfo:
        return self._member

    @property
    def PropertyFunc(self) -> Callable[[T], TProperty]:
        return self._PropertyFunc

    @property
    def Expression(self) -> LambdaExpression:
        return LambdaExpression(self._expression)

    @property
    def TypeToValidate(self) -> Type:
        return self._typeToValidate

    @property
    def HasCondition(self) -> bool:
        return self._condition is not None

    @property
    def HasAsyncCondition(self) -> bool:
        # TODOL: Checked
        return False
        # return self._asyncCondition is not None

    @property
    def Components(self) -> list[RuleComponent[T, TProperty]]:
        return self._components

    @property
    def Condition(self) -> Optional[Callable[[ValidationContext[T]], bool]]:
        """Condition for all validators in this rule."""
        return self._condition

    @property
    def PropertyName(self):
        return self._propertyName

    @PropertyName.setter
    def PropertyName(self, value: Optional[str]) -> None:
        self._propertyName = value
        self._propertyDisplayName = ExtensionsInternal.split_pascal_case(self._propertyName)

    @overload
    def SetDisplayName(self, name: str): ...
    @overload
    def SetDisplayName(self, name: Callable[[ValidationContext[T], str]]): ...

    def SetDisplayName(self, name: str | Callable[[ValidationContext[T], str]]):
        if callable(name):
            self._displayNameFactory = name
            self._displayName = None

        else:
            self._displayName = name
            self._displayNameFactory = None
        return None

    @property
    def Current(self) -> IRuleComponent:
        if not self._components:
            return None
        return self._components[-1]

    @property
    def MessageBuilder(self) -> Callable[[IMessageBuilderContext[T, TProperty]], str]:
        return self._MessageBuilder
    
    @MessageBuilder.setter
    def MessageBuilder(self, value: Callable[[IMessageBuilderContext[T, TProperty]], str]) -> None: 
        self._MessageBuilder = value

    @property
    def CascadeMode(self) -> CascadeMode:
        return self._cascadeModeThunk()

    @CascadeMode.setter
    def CascadeMode(self, value):
        self._cascadeModeThunk = lambda: value

    @property
    def RuleSets(self) -> list[str]:
        return self._rule_sets

    @RuleSets.setter
    def RuleSets(self, value: list[str]):
        self._rule_sets = value

    @property
    def DependentRules(self) -> list[IValidationRuleInternal[T]]:
        return self._DependentRules

    @DependentRules.setter
    def DependentRules(self, value: list[IValidationRuleInternal[T]]) -> None:
        self._DependentRules = value

    def ApplyCondition(self, predicate: Callable[[ValidationContext[T]], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators) -> None:
        # Default behaviour for when/unless as of v1.3 is to apply the condition to all previous validators in the chain.
        if applyConditionTo == ApplyConditionTo.AllValidators:
            for validator in self._components:
                validator.ApplyCondition(predicate)

            if self.DependentRules is not None:
                for dependentRule in self.DependentRules:
                    dependentRule.ApplyCondition(predicate, applyConditionTo)
        else:
            self.Current.ApplyCondition(predicate)

    # public void ApplyAsyncCondition(Func<ValidationContext<T>, CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
    # 	// Default behaviour for when/unless as of v1.3 is to apply the condition to all previous validators in the chain.
    # 	if (applyConditionTo == ApplyConditionTo.AllValidators) {
    # 		foreach (var validator in _components) {
    # 			validator.ApplyAsyncCondition(predicate);
    # 		}

    # 		if (DependentRules is not None) {
    # 			foreach (var dependentRule in DependentRules) {
    # 				dependentRule.ApplyAsyncCondition(predicate, applyConditionTo);
    # 			}
    # 		}
    # 	}
    # 	else {
    # 		Current.ApplyAsyncCondition(predicate);
    # 	}
    # }

    def ApplySharedCondition(self, condition: Callable[[ValidationContext[T]], bool]) -> None:
        if self._condition is None:
            self._condition = condition
        else:
            original = self._condition
            self._condition = lambda ctx: condition(ctx) and original(ctx)

    # public void ApplySharedAsyncCondition(Func<ValidationContext<T>, CancellationToken, Task<bool>> condition) {
    # 	if (_asyncCondition == null) {
    # 		_asyncCondition = condition;
    # 	}
    # 	else {
    # 		var original = _asyncCondition;
    # 		_asyncCondition = async (ctx, ct) => await condition(ctx, ct) && await original(ctx, ct);
    # 	}
    # }

    # object IValidationRule<T>.GetPropertyValue(T instance) => PropertyFunc(instance);

    @staticmethod
    def PrepareMessageFormatterForValidationError(context: ValidationContext[T], value: TValue) -> None:
        context.MessageFormatter.AppendPropertyName(context.DisplayName)
        context.MessageFormatter.AppendPropertyValue(value)
        context.MessageFormatter.AppendArgument("PropertyPath", context.PropertyPath)

    def CreateValidationError(
        self,
        context: ValidationContext[T],
        value: TValue,
        component: RuleComponent[T, TValue],
    ) -> ValidationFailure:
        if self.MessageBuilder is not None:
            error = self.MessageBuilder(MessageBuilderContext[T, TProperty](context, value, component))
        else:
            error = component.GetErrorMessage(context, value)

        failure = ValidationFailure(context.PropertyPath, error, value, component.ErrorCode)

        failure.FormattedMessagePlaceholderValues = context.MessageFormatter.PlaceholderValues.copy()
        failure.ErrorCode = component.ErrorCode if component.ErrorCode is not None else ValidatorOptions.Global.ErrorCodeResolver(component.Validator)

        failure.Severity = component.SeverityProvider(context, value) if component.SeverityProvider is not None else ValidatorOptions.Global.Severity

        if component.CustomStateProvider is not None:
            failure.CustomState = component.CustomStateProvider(context, value)

        # if (ValidatorOptions.Global.OnFailureCreated is not None):
        #     failure = ValidatorOptions.Global.OnFailureCreated(failure, context, value, self, component);

        return failure
