from typing import Callable, overload, override
from stc.common.scripts.FluentValidation.validators.AbstractComparisonValidator import AbstractComparisonValidator, Comparison

class MemberInfo: ... #    BORRAR clase cuando acabe


class GreaterThanValidator[T, TProperty](AbstractComparisonValidator[T, TProperty]):


    @overload
    def __init__(self, value:TProperty):...
    @overload
    def __init__(self, valueToCompareFunc: Callable[[T], TProperty], member:MemberInfo, memberDisplayName:str): ... 
    @overload
    def __init__(self, valueToCompareFunc:Callable[[T], tuple[bool,TProperty]], member:MemberInfo, memberDisplayName:str):...
    
    
    
    def __init__(self
            , value= None
            , valueToCompareFunc= None
            , member= None
            , memberDisplayName= None
            ):
        super().__init__(
              valueToCompareFunc= valueToCompareFunc
            , member= member
            , memberDisplayName= memberDisplayName
            , value= value
                )

    @override
    def is_valid(self, value:TProperty, valueToCompare:TProperty):
        if valueToCompare is None:
            return False

        return value > valueToCompare 
        # return value.CompareTo(valueToCompare) > 0
    
    @override
    def Comparison(self)->Comparison: Comparison.GreaterThan
