from abc import abstractmethod, ABC
from typing import Any, Self, TypeVar
import dis

from validators.IpropertyValidator import IPropertyValidator
from validators.LengthValidator import *
from validators.NotNullValidator import NotNullValidator
from validators.RegularExpressionValidator import RegularExpressionValidator
from validators.IsInstance import IsInstance
from validators.NotEmptyValidator import NotEmptyValidator

from validators.LessThanValidator import LessThanValidator
from validators.LessThanOrEqualValidator import LessThanOrEqualValidator
from validators.EqualValidator import EqualValidator
from validators.NotEqualValidator import NotEqualValidator
from validators.GreaterThanValidator import GreaterThanValidator
from validators.GreaterThanOrEqualValidator import GreaterThanOrEqualValidator
from IValidationRule import IValidationRule

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

	#region LessThan
	@overload
	def LessThan[TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:TProperty)->TIRuleBuilder: ...
	@overload
	def LessThan[T,TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:Callable[[T],TProperty])->TIRuleBuilder: ...
	
	def LessThan[T,TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:Callable[[T],TProperty]|TProperty)->TIRuleBuilder:
		if callable(valueToCompare):
			func = valueToCompare
			name = {x.opname:x.argval for x in dis.Bytecode(valueToCompare)}["LOAD_ATTR"]
			return ruleBuilder.SetValidator(LessThanValidator[T,TProperty](valueToCompareFunc=func, memberDisplayName=name))
		
		return  ruleBuilder.SetValidator(LessThanValidator(value = valueToCompare))
	#endregion
	#region LessThanOrEqual
	@overload
	def LessThanOrEqual[TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:TProperty)->TIRuleBuilder: ...
	@overload
	def LessThanOrEqual[T,TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:Callable[[T],TProperty])->TIRuleBuilder: ...
	
	def LessThanOrEqual[T,TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:Callable[[T],TProperty]|TProperty)->TIRuleBuilder:
		if callable(valueToCompare):
			func = valueToCompare
			name = {x.opname:x.argval for x in dis.Bytecode(valueToCompare)}["LOAD_ATTR"]
			return ruleBuilder.SetValidator(LessThanOrEqualValidator[T,TProperty](valueToCompareFunc=func, memberDisplayName=name))
		
		return  ruleBuilder.SetValidator(LessThanOrEqualValidator(value = valueToCompare))
	#endregion
	#region Equal
	@overload
	def Equal[TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:TProperty)->TIRuleBuilder: ...
	@overload
	def Equal[T,TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:Callable[[T],TProperty])->TIRuleBuilder: ...
	
	def Equal[T,TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:Callable[[T],TProperty]|TProperty)->TIRuleBuilder:
		if callable(valueToCompare):
			func = valueToCompare
			name = {x.opname:x.argval for x in dis.Bytecode(valueToCompare)}["LOAD_ATTR"]
			return ruleBuilder.SetValidator(EqualValidator[T,TProperty](valueToCompareFunc=func, memberDisplayName=name))
		
		return  ruleBuilder.SetValidator(EqualValidator(value = valueToCompare))
	#endregion
	#region NotEqual
	@overload
	def NotEqual[TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:TProperty)->TIRuleBuilder: ...
	@overload
	def NotEqual[T,TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:Callable[[T],TProperty])->TIRuleBuilder: ...
	
	def NotEqual[T,TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:Callable[[T],TProperty]|TProperty)->TIRuleBuilder:
		if callable(valueToCompare):
			func = valueToCompare
			name = {x.opname:x.argval for x in dis.Bytecode(valueToCompare)}["LOAD_ATTR"]
			return ruleBuilder.SetValidator(NotEqualValidator[T,TProperty](valueToCompareFunc=func, memberDisplayName=name))
		
		return  ruleBuilder.SetValidator(NotEqualValidator(value = valueToCompare))
	#endregion
	#region GreaterThan
	@overload
	def GreaterThan[TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:TProperty)->TIRuleBuilder: ...
	@overload
	def GreaterThan[T,TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:Callable[[T],TProperty])->TIRuleBuilder: ...
	
	def GreaterThan[T,TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:Callable[[T],TProperty]|TProperty)->TIRuleBuilder:
		if callable(valueToCompare):
			func = valueToCompare
			name = {x.opname:x.argval for x in dis.Bytecode(valueToCompare)}["LOAD_ATTR"]
			return ruleBuilder.SetValidator(GreaterThanValidator[T,TProperty](valueToCompareFunc=func, memberDisplayName=name))
		
		return  ruleBuilder.SetValidator(GreaterThanValidator(value = valueToCompare))
	#endregion
	#region GreaterThanOrEqual
	@overload
	def GreaterThanOrEqual[TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:TProperty)->TIRuleBuilder: ...
	@overload
	def GreaterThanOrEqual[T,TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:Callable[[T],TProperty])->TIRuleBuilder: ...
	
	def GreaterThanOrEqual[T,TProperty](ruleBuilder:TIRuleBuilder, valueToCompare:Callable[[T],TProperty]|TProperty)->TIRuleBuilder:
		if callable(valueToCompare):
			func = valueToCompare
			name = {x.opname:x.argval for x in dis.Bytecode(valueToCompare)}["LOAD_ATTR"]
			return ruleBuilder.SetValidator(GreaterThanOrEqualValidator[T,TProperty](valueToCompareFunc=func, memberDisplayName=name))
		
		return  ruleBuilder.SetValidator(GreaterThanOrEqualValidator(value = valueToCompare))
	#endregion




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

