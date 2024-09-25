from typing import Any, Callable, Type, get_type_hints, get_args, get_origin, Union
from fluent_validation.lambda_disassembler.tree_instruction import TreeInstruction, TupleInstruction


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
        original_type_hints: dict[str, Any] = get_type_hints(type_model.__init__)

        if not self._lambda_vars or len(original_type_hints) == 0:
            return None
        _, *nested_name = self._lambda_vars[0].nested_element.parents

        current_instance_var = None
        current_type_hints: dict[str, Any] = original_type_hints
        for var in nested_name:
            var_type_hint = current_type_hints[var]
            origin = get_origin(var_type_hint)
            if origin is Union:
                current_instance_var = get_args(var_type_hint)[0]
            else:
                current_instance_var = var_type_hint

            current_type_hints = get_type_hints(current_instance_var.__init__)
        return current_instance_var
