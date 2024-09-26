from typing import Any, Callable, Type, get_type_hints, get_args, get_origin, Union
from fluent_validation.lambda_disassembler.tree_instruction import TreeInstruction, TupleInstruction
import types


class MemberInfo:
    def __init__(self, func: Callable[..., Any]) -> None:
        self._func: Callable[..., Any] = func
        self._disassembler: TreeInstruction = TreeInstruction(func)
        self._lambda_vars: list[TupleInstruction] = self._disassembler.to_list()

        self._name: None | str = self.assign_name()

    @property
    def Name(self) -> str:
        return self._name

    def assign_name(self) -> str | None:
        if not self._lambda_vars:
            return None
        lambda_var, *nested_name = self._lambda_vars[0].nested_element.parents

        return lambda_var if not nested_name else nested_name[-1]

    def get_type_hint(self, type_model: Type) -> Type[Any]:
        current_type_hints: dict[str, Any] = get_type_hints(type_model.__init__)

        if not self._lambda_vars:
            return None

        lambda_var, *nested_name = self._lambda_vars[0].nested_element.parents

        if hasattr(type_model, self.Name) and isinstance(prop := getattr(type_model, self.Name), property):
            return get_type_hints(prop.fget)["return"]

        if len(current_type_hints) == 0:
            if lambda_var == self.Name:
                return get_origin(type_model)

            raise TypeError(f"The variable '{self.Name}' does not exist in '{type_model.__name__}' class")

        current_instance_var = None
        for var in nested_name:
            var_type_hint = current_type_hints[var]

            # It would be something like:   int | float | Decimal | ...
            if self.isUnionType(var_type_hint):
                return var_type_hint

            current_instance_var = self.get_args(var_type_hint)
            current_type_hints = get_type_hints(current_instance_var.__init__)
        return current_instance_var

    @staticmethod
    def isUnionType(value: Any) -> bool:
        return get_origin(value) is types.UnionType

    @staticmethod
    def isOptional(value: Any) -> bool:
        return get_origin(value) is Union

    @classmethod
    def get_args(cls, value: Any) -> Any:
        if cls.isOptional(value):
            return get_args(value)[0]
        return value
