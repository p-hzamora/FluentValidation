
from dataclasses import dataclass
from typing import Iterable

from results.ValidationFailure import ValidationFailure
from IValidationContext import ValidationContext


class ValidationResult[T]():
    def __init__(self,
                 errors:ValidationFailure= None,
                 failures:Iterable[ValidationFailure]=None
            ) -> None:
        if errors is None and failures is None:
            self.__init__no_args()

        elif errors is None and isinstance(failures,list):
            self.__init__iterable_validation_failure(failures)

        elif errors and not failures:
            self.__init__list_error_failure(errors)
        else:
            raise Exception(f"No se ha inicializado la clase {self.__class__.__name__}")
        
        

    def __init__no_args(self): 
        self._errors:list[ValidationFailure] = []

    def __init__iterable_validation_failure(self,failure:Iterable[ValidationFailure]):
        self._errors:list[ValidationFailure] = []
        for x in failure:
            if not x is None:
                self._errors.append(x)

    def __init__list_error_failure(self,errors:list[ValidationFailure]): 
        self._errors:list[ValidationFailure] = errors


    @property
    def is_valid(self)->bool: return len(self._errors) == 0

    @property
    def errors(self)->list[ValidationFailure]:
        return self._errors



