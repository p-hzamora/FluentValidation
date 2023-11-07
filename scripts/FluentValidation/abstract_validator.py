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




TAbstractValidator = TypeVar("TAbstractValidator",bound="AbstractValidator")
TRuleBuilder = TypeVar("TRuleBuilder",bound="RuleBuilder")
TPropertyRule = TypeVar("TPropertyRule",bound="PropertyRule")




class RuleBase[T,TProperty,TValue](IValidationRule[T,TValue]):
    def __init__(self,propertyFunc:Callable[[T],TProperty],type_to_validate:type):
        self._PropertyFunc = propertyFunc
        self._type_to_validate = type_to_validate
        
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
    def MessageBuilder(self)-> Callable[[IMessageBuilderContext[T,TProperty]],str]: None


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
    def __init__(self,func:Callable[[T],TProperty],type_to_validate:type):
        super().__init__(func,type_to_validate)

    @classmethod
    def create(cls, func:Callable[[T],TProperty])->Self:
        return PropertyRule(func,type(TProperty))

    def AddValidator(self,validator:IPropertyValidator[T,TProperty])->None:
        component:RuleComponent = RuleComponent[T,TProperty](validator)
        self._components.append(component)
        return None
    
    def GetDisplayName(): ...


    def ValidateAsync(self, context:ValidationContext[T])-> None:
        first = True
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
        self._rules:list[PropertyRule] = []

    def validate(self, instance:T)->ValidationResult:
        return self.internal_validate(ValidationContext(instance))


    def internal_validate(self, context:ValidationContext)->ValidationResult:
        for rule in self._rules:
            rule.ValidateAsync(context)
 
        result:ValidationResult = ValidationResult(None,context.Failures)
        # self.SetExecutedRuleSets(result,context)
        return result

    def RuleFor[TProperty](self,func:Callable[[T],TProperty])->IRuleBuilder[T,TProperty]: #IRuleBuilderInitial[T,TProperty]:
        rule:PropertyRule[T,TProperty] = PropertyRule.create(func)
        self._rules.append(rule)
        return RuleBuilder(rule,self)

    def SetExecutedRuleSets(self, result:ValidationResult, context:ValidationContext[T]):...
        #result.RuleSetExecuted = RulesetValidatorSelector.DefaultRuleSetNameInArray


class RegexPattern():
    Email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$"
    PhoneNumber = r"^\d{9}$"
    PostalCode = r"^\d{5}$"
    Dni = r"^[0-9]{8}[A-Z]$"







if __name__ == "__main__":
    @dataclass
    class Person():
        name:str
        dni:str
        email:str
        person_id:int =None


    class PersonValidator(AbstractValidator[Person]):
        def __init__(self) -> None:
            super().__init__()
            self.RuleFor(lambda x: x.dni).IsInstance(float).WithMessage("mensaje personalizado de is_instance").Matches(RegexPattern.PhoneNumber).Length(10,50).WithMessage("no tiene los caracteres exactos").Length(15,20).WithMessage("error personalizado de longitud")
            self.RuleFor(lambda x:x.email).NotNull().MaxLength(5).Matches(RegexPattern.Email).WithMessage("El correo introducido no cumple con la regex especifica").MaxLength(5).WithMessage("El correo excede los 5 caracteres")
            pass


    person = Person(name="Pablo",dni="51527736P",email="pablogmail.org")

    validator = PersonValidator()
    result = validator.validate(person)
    if not result.is_valid:
        for error in result.errors:
            print(f"Error en {error.PropertyName} con mensaje:\t{error.ErrorMessage}")