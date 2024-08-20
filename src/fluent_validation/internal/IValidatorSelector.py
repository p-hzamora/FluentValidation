from abc import abstractmethod, ABC

from src.fluent_validation.IValidationContext import IValidationContext
from src.fluent_validation.IValidationRule import IValidationRule

class IValidatorSelector(ABC):
	@abstractmethod
	def CanExecute(self, rule: IValidationRule, propertyPath:str, context: IValidationContext)->bool:...