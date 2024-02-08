from abc import ABC, abstractmethod

from .results.ValidationResult import ValidationResult


class IValidator[T](ABC):
    @abstractmethod
    def Validate(instance: T) -> ValidationResult:
        ...
