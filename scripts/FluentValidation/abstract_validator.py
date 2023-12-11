from abc import ABC
from typing import Any, Callable, List, TypeVar, overload
import dis


from dataclasses import dataclass
from IValidationRule import IValidationRule
from internal.MessageBuilderContext import MessageBuilderContext
from internal.RuleComponent import RuleComponent
from results.ValidationFailure import ValidationFailure


from validators.IpropertyValidator import IPropertyValidator
from results.ValidationResult import ValidationResult
from IValidationContext import ValidationContext
from IValidationRule import *
from syntax import *
from DefaultValidatorExtensions import CascadeMode, ValidatorOptions




TAbstractValidator = TypeVar("TAbstractValidator",bound="AbstractValidator")
TRuleBuilder = TypeVar("TRuleBuilder",bound="RuleBuilder")
TPropertyRule = TypeVar("TPropertyRule",bound="PropertyRule")



class RuleBase[T,TProperty,TValue](IValidationRule[T,TValue]):
    def __init__(self,propertyFunc:Callable[[T],TProperty], cascadeModeThunk:Callable[[],CascadeMode], type_to_validate:type):
        self._PropertyFunc = propertyFunc
        self._type_to_validate = type_to_validate
        self._cascadeModeThunk:Callable[[],CascadeMode] = cascadeModeThunk
        self._components:List[RuleComponent[T, TProperty]] = []
        self._propertyName:str = {x.opname:x.argval for x in dis.Bytecode(propertyFunc)}["LOAD_ATTR"]
        self._displayName:str = self._propertyName

    @property
    def PropertyFunc(self)->Callable[[T],TProperty]: return self._PropertyFunc
    @property
    def TypeToValidate(self): return self._type_to_validate

    @property
    def Components(self): return self._components

    @property
    def PropertyName(self): return self._propertyName
    
    @property
    def displayName(self): return self._displayName

    @property
    def Current(self)->IRuleComponent: return self._components[-1]

    @property
    @property
    def CascadeMode(self)-> Callable[[],CascadeMode]: return self._cascadeModeThunk()
    @CascadeMode.setter
    def CascadeMode(self,value): lambda: value


    @staticmethod
    def PrepareMessageFormatterForValidationError(context:ValidationContext[T], value:TValue)->None:
        # context.MessageFormatter.AppendPropertyName(context.DisplayName)
        context.MessageFormatter.AppendPropertyValue(value)
        # context.MessageFormatter.AppendArgument("PropertyPath", context.PropertyPath)



    def CreateValidationError(self, context:ValidationContext[T], value:TValue, component:RuleComponent[T, TValue])->ValidationFailure: 
        if self.MessageBuilder is not None:
            error =self.MessageBuilder(MessageBuilderContext[T,TProperty](context,value,component))
        else:
            error = component.GetErrorMessage(context,value)

        failure = ValidationFailure(context.PropertyPath, error, value,component.ErrorCode)

        # failure.FormattedMessagePlaceholderValues = context.MessageFormatter.PlaceholderValues
        failure._ErrorCode = component.ErrorCode # ?? ValidatorOptions.Global.ErrorCodeResolver(component.Validator);

        return failure



class PropertyRule[T,TProperty](RuleBase[T,TProperty,TProperty]):
    def __init__(self
                 , func:Callable[[T],TProperty]
                 , cascadeModeThunk:Callable[[],CascadeMode]
                 , type_to_validate:type
                )->None:
        super().__init__(func, cascadeModeThunk, type_to_validate)


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
            if len(context.Failures)> total_failures and cascade == CascadeMode.Stop:
                break

        return None
    

class RuleBuilder[T,TProperty](IRuleBuilder,IRuleBuilderInternal): # no implemento IRuleBuilderOptions por que el metodo no se que hace

    def __init__(self,rule:IValidationRuleInternal[T,TProperty], parent:TAbstractValidator):
        self._rule = rule
        self.parent_validator = parent

    def SetValidator(self,validator:IPropertyValidator[T,TProperty])->IRuleBuilder[T,TProperty]: # -> IRuleBuilderOptions[T,TProperty]
        self.Rule.AddValidator(validator)
        return self
    
    @property
    def Rule(self) -> IValidationRule[T, TProperty]:
        return self._rule
        

class AbstractValidator[T](ABC):
    def __init__(self) -> None:
        self._classLevelCascadeMode:Callable[[],CascadeMode] = lambda : ValidatorOptions.Global.DefaultClassLevelCascadeMode
        self._ruleLevelCascadeMode:Callable[[],CascadeMode] = lambda : ValidatorOptions.Global.DefaultRuleLevelCascadeMode
        self._rules:list[PropertyRule] = []

    def validate(self, instance:T)->ValidationResult:
        return self.internal_validate(ValidationContext(instance))


    def internal_validate(self, context:ValidationContext)->ValidationResult:
        for rule in self._rules:
            rule.ValidateAsync(context)
            if self.ClassLevelCascadeMode== CascadeMode.Stop and len(result.errors)> 0:
                break
 
        result:ValidationResult = ValidationResult(None,context.Failures)
        # self.SetExecutedRuleSets(result,context)
        return result

    def RuleFor[TProperty](self,func:Callable[[T],TProperty])->IRuleBuilder[T,TProperty]: #IRuleBuilderInitial[T,TProperty]:
        rule:PropertyRule[T,TProperty] = PropertyRule.create(func, lambda: self.RuleLevelCascadeMode)
        self._rules.append(rule)
        return RuleBuilder(rule,self)
    @property
    def ClassLevelCascadeMode(self)->CascadeMode:
        return self._classLevelCascadeMode()
    @ClassLevelCascadeMode.setter
    def ClassLevelCascadeMode(self, value): self._classLevelCascadeMode = lambda: value


    @property
    def RuleLevelCascadeMode(self)->CascadeMode:
        return self._ruleLevelCascadeMode()
    @RuleLevelCascadeMode.setter
    def RuleLevelCascadeMode(self, value): self._ruleLevelCascadeMode = lambda: value
