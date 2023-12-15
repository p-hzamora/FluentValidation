from typing import Callable, overload, override
from stc.common.scripts.FluentValidation.validators.AbstractComparisonValidator import AbstractComparisonValidator, Comparison


class NotEqualValidator[T, TProperty](AbstractComparisonValidator[T, TProperty]):
    @overload
    def __init__(self, value:TProperty):...
    @overload
    def __init__(self, valueToCompareFunc: Callable[[T], TProperty], memberDisplayName:str): ... 
    @overload
    def __init__(self, valueToCompareFunc:Callable[[T], tuple[bool,TProperty]], memberDisplayName:str):...
    
    def __init__(self
            , value= None
            , valueToCompareFunc= None
            , memberDisplayName= None
            ):
        super().__init__(
              valueToCompareFunc= valueToCompareFunc    
            , memberDisplayName= memberDisplayName
            , value= value
                )
    
    @override
    @property
    def Comparison(self)->Comparison: return Comparison.NotEqual