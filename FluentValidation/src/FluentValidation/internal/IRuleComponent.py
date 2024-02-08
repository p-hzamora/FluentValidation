from abc import ABC, abstractmethod

from ..validators.IpropertyValidator import IPropertyValidator


class IRuleComponent(ABC):
    @property
    @abstractmethod
    def ErrorCode(self) -> str:
        ...

    @property
    @abstractmethod
    def Validator(self) -> IPropertyValidator:
        ...

    @abstractmethod
    def set_error_message(error_message: str):
        ...
