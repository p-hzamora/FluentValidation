from abc import abstractmethod, ABC
from typing import Any, Self, TypeVar
from IValidationRule import IValidationRule

from validators.IpropertyValidator import IPropertyValidator
from validators.LengthValidator import *
from validators.NotNullValidator import NotNullValidator
from validators.RegularExpressionValidator import RegularExpressionValidator
from validators.IsInstance import IsInstance
from validators.NotEmptyValidator import NotEmptyValidator

TIRuleBuilder = TypeVar("TIRuleBuilder",bound="IRuleBuilder")




class DefaultValidatorExtensions:
	"""
	ruleBuilder actua como self, ya que es la instancia padre que se le pasa a traves de la herencia
	"""
	def configurable[T,TProperty](ruleBuilder:TIRuleBuilder)->IValidationRule[T,TProperty]:
		return ruleBuilder.Rule
	
	def NotNull[T, TProperty](ruleBuilder:TIRuleBuilder)->TIRuleBuilder:
		return ruleBuilder.SetValidator(NotNullValidator[T,TProperty]())

	def Matches[T](ruleBuilder:TIRuleBuilder, pattern:str)->TIRuleBuilder:
		return ruleBuilder.SetValidator(RegularExpressionValidator[T](pattern))

	def Length[T](ruleBuilder:TIRuleBuilder, min:int,max:int)->TIRuleBuilder:
		return ruleBuilder.SetValidator(LengthValidator[T](min,max))

	def ExactLength[T](ruleBuilder:TIRuleBuilder, exactLength:int)->TIRuleBuilder:
		return ruleBuilder.SetValidator(ExactLengthValidator[T](exactLength))

	def MaxLength[T](ruleBuilder:TIRuleBuilder, MaxLength:int)->TIRuleBuilder:
		return ruleBuilder.SetValidator(MaximumLengthValidator[T](MaxLength))

	def MinLength[T](ruleBuilder:TIRuleBuilder, MinLength:int)->TIRuleBuilder:
		return ruleBuilder.SetValidator(MinimumLengthValidator[T](MinLength))

	def IsInstance[T](ruleBuilder:TIRuleBuilder, instance:Any)->TIRuleBuilder:
		return ruleBuilder.SetValidator(IsInstance[T](instance))

	def WithMessage(ruleBuilder:TIRuleBuilder,errorMessage:str)->TIRuleBuilder:
		DefaultValidatorExtensions.configurable(ruleBuilder).Current.set_error_message(errorMessage)
		return ruleBuilder

	def NotEmpty[T, TProperty](ruleBuilder:TIRuleBuilder)->TIRuleBuilder:
		return ruleBuilder.SetValidator(NotEmptyValidator[T, TProperty]())



class IRuleBuilderInternal[T,TProperty](ABC):
	@property
	@abstractmethod
	def Rule(self)-> IValidationRule[T,TProperty]: ...


class IRuleBuilder[T, TProperty] (IRuleBuilderInternal, DefaultValidatorExtensions):
	@staticmethod
	@abstractmethod
	def SetValidator(validator: IPropertyValidator[T, TProperty])->Self: ...



class IRuleBuilderOptions[T,TProperty](IRuleBuilder[T, TProperty]):
    @abstractmethod
    def DependentRules(action)->Self: ...

