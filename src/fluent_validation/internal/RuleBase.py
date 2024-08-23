from typing import Callable, List, Optional

from src.fluent_validation.ValidatorOptions import ValidatorOptions
from src.fluent_validation.internal.ExtensionInternal import ExtensionsInternal

from ..IValidationRule import IValidationRule, IRuleComponent
from ..internal.MessageBuilderContext import IMessageBuilderContext, MessageBuilderContext
from ..internal.RuleComponent import RuleComponent
from ..results.ValidationFailure import ValidationFailure


from ..IValidationContext import ValidationContext
from ..enums import CascadeMode


class RuleBase[T, TProperty, TValue](IValidationRule[T, TValue]):
    def __init__(
        self,
        propertyFunc: Callable[[T], TProperty],
        cascadeModeThunk: Callable[[], CascadeMode],
        type_to_validate: type,
    ):
        self._PropertyFunc = propertyFunc
        self._cascadeModeThunk: Callable[[], CascadeMode] = cascadeModeThunk
        # TODOL: Check if I've to use the same code for 'self._propertyName' and 'self.displayNameFastory'
        self._propertyName: Optional[str] = ValidatorOptions.Global.PropertyNameResolver(propertyFunc).to_list()[0].nested_element.name
        self._displayNameFactory: Callable[[ValidationContext[T], str]] = lambda context: ValidatorOptions.Global.PropertyNameResolver(propertyFunc).to_list()[0].nested_element.name

        self._displayNameFunc: Callable[[ValidationContext[T], str]] = self.get_display_name

        self._type_to_validate = type_to_validate
        self._components: List[RuleComponent[T, TProperty]] = []

        self._propertyDisplayName: Optional[str] = None

        self._displayName: str = self._propertyName  # FIXME [x]: This implementation is wrong. It must call the "GetDisplay" method
        self._rule_sets: Optional[list[str]] = None

    def get_display_name(self, context: ValidationContext[T]) -> None | str:
        if self._displayNameFactory is not None and (res := self._displayNameFactory(context)) is not None:
            return res
        elif self._displayName:
            return self.displayName
        else:
            return self._propertyDisplayName

    @property
    def PropertyFunc(self) -> Callable[[T], TProperty]:
        return self._PropertyFunc

    @property
    def TypeToValidate(self):
        return self._type_to_validate

    @property
    def Components(self):
        return self._components

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
        return self._components[-1]

    @property
    def MessageBuilder(self) -> Callable[[IMessageBuilderContext[T, TProperty]], str]:
        return None

    @property
    def CascadeMode(self) -> CascadeMode:
        return self._cascadeModeThunk()

    @CascadeMode.setter
    def CascadeMode(self, value):
        lambda: value

    @property
    def RuleSets(self) -> list[str]:
        return self._rule_sets

    @RuleSets.setter
    def RuleSets(self, value: list[str]):
        self._rule_sets = value

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

        failure.FormattedMessagePlaceholderValues = context.MessageFormatter.PlaceholderValues
        failure._ErrorCode = component.ErrorCode  # ?? ValidatorOptions.Global.ErrorCodeResolver(component.Validator);

        return failure
