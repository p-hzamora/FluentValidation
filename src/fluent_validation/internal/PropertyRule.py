from __future__ import annotations
from typing import Callable, Self, TYPE_CHECKING

from ..enums import CascadeMode
from ..internal.RuleBase import RuleBase
from ..internal.RuleComponent import RuleComponent

if TYPE_CHECKING:
    from ..validators.IpropertyValidator import IPropertyValidator
    from ..IValidationContext import ValidationContext


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

    async def ValidateAsync(self, context: ValidationContext[T], useAsync: bool) -> None:
        displayName: None | str = self.get_display_name(context)

        if self.PropertyName is None and displayName is None:
            displayName = ""

        PropertyPath: str = context.PropertyChain.BuildPropertyPath(displayName if not self.PropertyName else self.PropertyName)
        if not context.Selector.CanExecute(self, PropertyPath, context):
            return None

        if self.Condition:
            if not self.Condition(context):
                return None

        # if (AsyncCondition != null) {
        #     if (useAsync) {
        #         if (!await AsyncCondition(context, cancellation)) {
        #             return;
        #         }
        #     }
        #     else {
        #         throw new AsyncValidatorInvokedSynchronouslyException();
        #     }
        # }

        first = True

        cascade = self.CascadeMode
        total_failures = len(context.Failures)

        context.InitializeForPropertyValidator(PropertyPath, self._displayNameFunc, self.PropertyName)

        for component in self.Components:
            context.MessageFormatter.Reset()

            if not component.InvokeCondition(context):
                continue

            # if component.HasAsyncCondition:
            #     if useAsync:
            #         if await component.invokeAsyncCondition(context,cancellation):
            #             continue
            #         else:
            #             raise Exception # AsyncValidatorInvokedSynchrouslyException

            if first:
                first = False
                try:
                    propValue = self.PropertyFunc(context.instance_to_validate)
                except AttributeError:  # FIXME [ ]: Checked this try/except
                    AttributeError("NullReferenceException occurred when executing rule for 'self.Expression'. If this property can be null you should add a null check using a When condition")

            valid: bool = await component.ValidateAsync(context, propValue, useAsync)
            if not valid:
                self.PrepareMessageFormatterForValidationError(context, propValue)
                failure = self.CreateValidationError(context, propValue, component)
                context.Failures.append(failure)

            if len(context.Failures) > total_failures and cascade == CascadeMode.Stop:
                break

            # if len(context.Failures) <= total_failures & self.DependentRules is not None:
            #     for dependentRule in self.DependentRules:
            #         await dependentRule.ValidateAsync(context,useAsync)

        # if len(context.Failures) <= total_failures and self.DependentRules is not None:
        #     for dependentRules in self.DependentRules:
        #         await dependentRules.ValidateAsync(context,useAsync)
        return None
