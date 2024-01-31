
from ..IValidationContext import ValidationContext
from ..internal.IRuleComponent import IRuleComponent
from ..validators.IpropertyValidator import IPropertyValidator


class RuleComponent[T,TProperty](IRuleComponent):
    def __init__(self,property_validator:IPropertyValidator[T,TProperty]) -> None:
        self._property_validator:IPropertyValidator[T,TProperty]= property_validator
        self._error_message = property_validator.get_default_message_template()

    def __repr__(self) -> str:
        return f"<RuleComponent validator: {self.ErrorCode}>"

    @property
    def ErrorCode(self)->str: return self._property_validator.__class__.__name__ # Nombre de la clase del validador 
    
    @property
    def Validator(self)-> IPropertyValidator: return self._property_validator # falta implementar => (IPropertyValidator) _propertyValidator ?? _asyncPropertyValidator;

    def set_error_message(self,error_message:str)-> None:
        self._error_message = error_message

    def invoke_property_validator(self, context:ValidationContext[T],value:TProperty)-> bool:
        return self.Validator.is_valid(context,value)

    def ValidateAsync(self, context:ValidationContext[T], value:TProperty)-> bool:
        return self.invoke_property_validator(context,value)

    def GetErrorMessage(self, context:ValidationContext[T], value:TProperty):
        rawTemplate:str = self._error_message

        if rawTemplate is None:
            # rawTemplate = self.Validator.get_default_messagke_template(self.ErrorCode) # original
            rawTemplate = self.Validator.get_default_message_template()

        if context is None:
            return rawTemplate
        
        return context.MessageFormatter.BuildMessage(rawTemplate)



