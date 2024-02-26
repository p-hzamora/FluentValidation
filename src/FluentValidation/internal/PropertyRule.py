from typing import Callable, Self

from ..enums import CascadeMode
from ..IValidationContext import ValidationContext
from ..internal.RuleBase import RuleBase
from ..internal.RuleComponent import RuleComponent
from ..validators.IpropertyValidator import IPropertyValidator


class PropertyRule[T, TProperty](RuleBase[T, TProperty, TProperty]):
    def __init__(
        self,
        func: Callable[[T], TProperty],
        cascadeModeThunk: Callable[[], CascadeMode],
        type_to_validate: type,
    ) -> None:
        super().__init__(func, cascadeModeThunk, type_to_validate)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} from '{self.PropertyName}' at {hex(id(self))}>"

    @classmethod
    def create(cls, func: Callable[[T], TProperty], cascadeModeThunk: Callable[[], CascadeMode]) -> Self:
        return PropertyRule(func, cascadeModeThunk, type(TProperty))

    def AddValidator(self, validator: IPropertyValidator[T, TProperty]) -> None:
        component: RuleComponent = RuleComponent[T, TProperty](validator)
        self._components.append(component)
        return None

    def get_display_name():
        ...

    def ValidateAsync(self, context: ValidationContext[T]) -> None:
        first = True
        total_failures = len(context.Failures)
        context.InitializeForPropertyValidator(self.PropertyName, self._displayName)
        for component in self.Components:
            context.MessageFormatter.Reset()
            if first:
                first = False
                propValue = self.PropertyFunc(context.instance_to_validate)

            valid: bool = component.ValidateAsync(context, propValue)
            if not valid:
                self.PrepareMessageFormatterForValidationError(context, propValue)
                failure = self.CreateValidationError(context, propValue, component)
                context.Failures.append(failure)
            if len(context.Failures) > total_failures and self.CascadeMode == CascadeMode.Stop:
                break

        return None
