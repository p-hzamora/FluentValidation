from typing import Callable, List
import dis

from ..IValidationRule import IValidationRule, IRuleComponent, IMessageBuilderContext
from ..internal.MessageBuilderContext import MessageBuilderContext
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
        self._type_to_validate = type_to_validate
        self._cascadeModeThunk: Callable[[], CascadeMode] = cascadeModeThunk
        self._components: List[RuleComponent[T, TProperty]] = []
        self._propertyName: str = {x.opname: x.argval for x in dis.Bytecode(propertyFunc)}["LOAD_ATTR"]
        self._displayName: str = self._propertyName  # FIXME [ ]: This implementation is wrong. It must call the "GetDisplay" method

        # public string get_display_name(ValidationContext<T> context)
        #     => _displayNameFactory?.Invoke(context) ?? _displayName ?? _propertyDisplayName;

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

    @property
    def displayName(self):
        return self._displayName

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
