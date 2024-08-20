from abc import abstractmethod, ABC

from src.FluentValidation.IValidationContext import IValidationContext
from src.FluentValidation.IValidationRule import IValidationRule

class IValidatorSelector(ABC):
	@abstractmethod
	def CanExecute(rule: IValidationRule, propertyPath:str, context: IValidationContext)->bool:...