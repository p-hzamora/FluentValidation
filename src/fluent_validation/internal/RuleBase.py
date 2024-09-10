from __future__ import annotations
from typing import Any, Callable, Type, Optional, TYPE_CHECKING

from src.fluent_validation.MemberInfo import MemberInfo
from src.fluent_validation.ValidatorOptions import ValidatorOptions
from src.fluent_validation.internal.ExtensionInternal import ExtensionsInternal
from ..IValidationRule import IValidationRule
from ...fluent_validation.internal.IRuleComponent import IRuleComponent
from ..internal.MessageBuilderContext import IMessageBuilderContext, MessageBuilderContext
from ..internal.RuleComponent import RuleComponent
from ..results.ValidationFailure import ValidationFailure


from ..IValidationContext import ValidationContext
from ..enums import ApplyConditionTo, CascadeMode

if TYPE_CHECKING:
    from src.fluent_validation.IValidationRuleInternal import IValidationRuleInternal
    from src.fluent_validation.validators.IpropertyValidator import IAsyncPropertyValidator, IPropertyValidator


class RuleBase[T, TProperty, TValue](IValidationRule[T, TValue]):
    def __init__(
        self,
        member: MemberInfo,
        propertyFunc: Callable[[T], TProperty],
        expression: Callable[..., Any],
        cascadeModeThunk: Callable[[], CascadeMode],
        typeToValidate: Type,
    ):
        self._member: MemberInfo = member
        self._PropertyFunc = propertyFunc
        self._expression: Callable[..., Any] = expression
        self._typeToValidate: Type = typeToValidate
        self._cascadeModeThunk: Callable[[], CascadeMode] = cascadeModeThunk

        containerType = type(T)
        self._propertyName: Optional[str] = ValidatorOptions.Global.PropertyNameResolver(containerType, member, expression)
        self._displayNameFactory: Callable[[ValidationContext[T], str]] = lambda context: ValidatorOptions.Global.DisplayNameResolver(containerType, member, expression)

        self._displayNameFunc: Callable[[ValidationContext[T], str]] = self.get_display_name

        self._components: list[RuleComponent[T, TProperty]] = []
        self._condition: Optional[Callable[[ValidationContext[T]], bool]] = None
        self._propertyDisplayName: Optional[str] = None

        self._displayName: str = self._propertyName  # FIXME [x]: This implementation is wrong. It must call the "GetDisplay" method
        self._rule_sets: Optional[list[str]] = None
        self._DependentRules: list[IValidationRuleInternal[T]] = None

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
        elif self._displayName:
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
    def Expression(self) -> Callable[..., Any]:
        return self._expression

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
    def PropertyName(self) -> Optional[str]:
        return self._propertyName

    @property
    def displayName(self, value: str):
        self._displayName = value
        self._propertyDisplayName = ExtensionsInternal.split_pascal_case(self._propertyName)

    @property
    def Current(self) -> IRuleComponent:
        if not self._components:
            return None
        return self._components[-1]

    @property
    def MessageBuilder(self) -> Callable[[IMessageBuilderContext[T, TProperty]], str]:
        return None

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

    # 		if (DependentRules != null) {
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
        failure._ErrorCode = component.ErrorCode if component.ErrorCode is not None else ValidatorOptions.Global.ErrorCodeResolver(component.Validator)

        return failure
