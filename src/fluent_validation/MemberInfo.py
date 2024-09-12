from typing import Any, Callable

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
