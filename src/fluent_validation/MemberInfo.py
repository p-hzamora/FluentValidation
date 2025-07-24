# region License
# Copyright (c) .NET Foundation and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# The latest version of this file can be found at https://github.com/p-hzamora/FluentValidation
# endregion

import inspect
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
        def get_types(obj: Any):
            init_types = get_type_hints(obj.__init__) if hasattr(obj, "__init__") else {}
            annotations_types = obj.__annotations__ if hasattr(obj, "__annotations__") else {}

            functions_dict = {name: obj for name, obj in inspect.getmembers(type_model, predicate=inspect.isfunction)}

            dict_types = init_types if len(init_types) > len(annotations_types) else annotations_types

            dict_types.update(functions_dict)
            return dict_types

        current_type_hints: dict[str, Any] = get_types(type_model)

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
            current_type_hints = get_types(current_instance_var)
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
