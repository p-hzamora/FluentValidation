from typing import TypeVar

from IValidationRule import IValidationRule
from validators.IpropertyValidator import IPropertyValidator
from IValidationRule import *
from syntax import *



TAbstractValidator = TypeVar("TAbstractValidator")



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
        
