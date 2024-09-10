from collections import defaultdict
from typing import Any, Callable, NamedTuple, Self, Optional
from dis import Instruction, Bytecode
from .dis_types import OpName
from .nested_element import NestedElement


from enum import Enum


class ConditionType(Enum):
    EQUAL = "=="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN_OR_EQUAL = ">="
    NOT_EQUAL = "!="
    REGEXP = "REGEXP"
    BETWEEN = "BETWEEN"
    LIKE = "LIKE"
    IN = "IN"
    IS = "IS"
    IS_NOT = "IS NOT"


class Node[T]:
    def __init__(self, data: T):
        self.data: T = data
        self.children: list[Self[T]] = []

    def __repr__(self) -> str:
        return f"{Node.__name__}: data={self.data} children={self.children}"


class TupleInstruction(NamedTuple):
    var: str
    nested_element: NestedElement[str]


class TreeInstruction:
    _FIRST_LEVEL: tuple[OpName] = (
        OpName.LOAD_FAST,
        OpName.LOAD_GLOBAL,
        OpName.LOAD_CONST,
        OpName.LOAD_DEREF,
    )

    def __init__[T, *Ts](self, lambda_: Callable[[T, *Ts], None]):
        self._root: Node[Instruction] = Node[Instruction](None)

        self._bytecode: Bytecode = Bytecode(lambda_)  # FIXME [ ]: don't know how to disassemble NoneType objects
        self._compare_op: Optional[list[str]] = []
        self._set_root()

    def __repr__(self) -> str:
        return f"{TreeInstruction.__name__} < at {hex(id(self))}>"

    @staticmethod
    def _transform__compare_op(compare_sybmol: ConditionType) -> str:
        dicc_symbols: dict[ConditionType, str] = {
            ConditionType.EQUAL: "=",
        }
        return dicc_symbols.get(compare_sybmol, compare_sybmol.value)

    @staticmethod
    def _transform_is_is_not(instr: Instruction) -> str:
        if instr.argval == 1:
            return ConditionType.IS_NOT.value
        elif instr.argval == 0:
            return ConditionType.IS.value
        else:
            raise Exception(f"argval value '{instr.argval}' not expected.")

    def _set_root(self) -> None:
        """
        add instructions into self._root
        """

        def is_instruction_comparable(instr: Instruction) -> bool:
            opname = OpName(instr.opname)
            if opname in (OpName.COMPARE_OP, OpName.IS_OP):
                return True
            return False

        def set_comparable(instr: Instruction) -> None:
            opname = OpName(instr.opname)
            if opname == OpName.COMPARE_OP:
                return self._compare_op.append(self._transform__compare_op(ConditionType(x.argval)))
            elif opname == OpName.IS_OP:
                return self._compare_op.append(self._transform_is_is_not(x))
            return None

        for x in self._bytecode:
            if is_instruction_comparable(x):
                set_comparable(x)
            else:
                self.add_instruction(x)

    def to_dict(self) -> dict[str, list[NestedElement[str]]]:
        _dict: dict[str, list[NestedElement[str]]] = defaultdict(list)
        for node in self.root.children:
            argval = self._join_data_attributes_from_node(node)
            _dict[node.data.argval].append(NestedElement[str](argval))
        return _dict

    def add_instruction(self, ins: Instruction) -> None:
        opname = OpName(ins.opname)
        if opname in TreeInstruction._FIRST_LEVEL:
            self._root.children.append(Node[Instruction](ins))
            return None

        if OpName(ins.opname) == OpName.LOAD_ATTR:
            last_fast_node = self._root.children[-1]
            new_node = Node[Instruction](ins)
            self._add_node(last_fast_node, new_node)
        return None

    def _add_node(self, parent_node: Node[Instruction], new_node: Node[Instruction]):
        parent_node.children.append(new_node)
        return None

    def get_all_nodes_of(self, node: Node[Instruction]) -> list[Node[Optional[Instruction]]]:
        def get_all_nodes(node: Node[Instruction], list: list[Node[Instruction]]):
            if not node.children:
                return list
            for subnode in node.children:
                if not subnode.children:
                    data = subnode
                else:
                    data = self.get_all_nodes_of(subnode)
                list.append(data)

        lista = []
        get_all_nodes(node, lista)
        return lista

    def to_list(self) -> list[TupleInstruction]:
        """
        Return list with tuple as data.
        This tuple contains the variable name as the first element and all children as the second one, all inside a TupleInstruction NamedTuple.
        """
        _list: list[list[NestedElement[str]]] = []
        for node in self.root.children:
            argval = self._join_data_attributes_from_node(node)
            _list.append(TupleInstruction(node.data.argval, NestedElement[str](argval)))
        return _list

    def _join_data_attributes_from_node(self, _node: Node[Instruction]) -> list[Any]:
        lista = self.get_all_nodes_of(_node)
        if not lista:
            return _node.data.argval
        else:
            # We just want to retrieve argval not Instruction object itself
            return [_node.data.argval] + [x.data.argval for x in lista]

    @property
    def root(self) -> Node[Instruction]:
        return self._root

    @property
    def compare_op(self) -> Optional[list[str]]:
        return self._compare_op
