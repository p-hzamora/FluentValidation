
from typing import Callable, Self

from stc.common.scripts.FluentValidation.DefaultValidatorExtensions import CascadeMode
from stc.common.scripts.FluentValidation.IValidationContext import ValidationContext
from stc.common.scripts.FluentValidation.internal.RuleBase import RuleBase
from stc.common.scripts.FluentValidation.internal.RuleComponent import RuleComponent
from stc.common.scripts.FluentValidation.validators.IpropertyValidator import IPropertyValidator


class PropertyRule[T,TProperty](RuleBase[T,TProperty,TProperty]):
    def __init__(self
                 , func:Callable[[T],TProperty]
                 , cascadeModeThunk:Callable[[],CascadeMode]
                 , type_to_validate:type
                )->None:
        super().__init__(func, cascadeModeThunk, type_to_validate)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} from '{self.PropertyName}' at {hex(id(self))}>"

    @classmethod
    def create(cls, func:Callable[[T],TProperty], cascadeModeThunk:Callable[[],CascadeMode] )->Self:
        return PropertyRule(func, cascadeModeThunk, type(TProperty))

    def AddValidator(self,validator:IPropertyValidator[T,TProperty])->None:
        component:RuleComponent = RuleComponent[T,TProperty](validator)
        self._components.append(component)
        return None
    
    def GetDisplayName(): ...


    def ValidateAsync(self, context:ValidationContext[T])-> None:
        first = True
        cascade = self.CascadeMode
        total_failures = len(context.Failures)
        context.InitializeForPropertyValidator(self.PropertyName)
        for component in self.Components:
            context.MessageFormatter.Reset()
            if first:
                first = False
                propValue= self.PropertyFunc(context.instance_to_validate)

            valid:bool = component.ValidateAsync(context,propValue)
            if not valid:
                # super().PrepareMessageFormatterForValidationError(context,propValue)
                failure = self.CreateValidationError(context,propValue,component)
                context.Failures.append(failure)
            #FIXME [ ] al modificar ClassLevelCascade fuera de esta clase, el enum no es el mismo pues no tiene la misma direccion en memoria
            if len(context.Failures)> total_failures and cascade == CascadeMode.Stop:
                break

        return None
   