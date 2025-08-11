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

from enum import Enum
from typing import Any, Callable, Iterable, Optional, Type, get_type_hints, get_args, get_origin, Union, overload
from fluent_validation.lambda_disassembler.tree_instruction import TreeInstruction, TupleInstruction
import types


class MemberInfo[T]:
    @overload
    def __init__(self, func: Callable[[T], Any], model: T) -> None: ...
    @overload
    def __init__(self, func: Callable[..., Any]) -> None: ...

    def __init__(self, func: Callable[[T], Any], model: Optional[T] = None) -> None:
        self._nested_names: list[str] = []

        self._model = model
        self._func: Callable[[T], Any] = func
        self._disassembler: TreeInstruction = TreeInstruction(func)
        self._lambda_vars: list[TupleInstruction] = self._disassembler.to_list()

        self._name: Optional[str] = self.assign_name()

    @property
    def Name(self) -> Optional[str]:
        return self._name

    @property
    def NestedNames(self) -> str:
        return self._nested_names

    def assign_name(self) -> Optional[list[str] | str]:
        if self._model:
            try:
                obj = self._func(self._model)

                # If "__name__" attribute is implemented we can return the name without working with lambda function in string.
                # COMMENT: This method allow us to use 'cast' method from typing when working with 'rule_for'
                if not isinstance(obj, type) and hasattr(obj, "__name__"):
                    return obj.__name__

            except AttributeError:
                pass

        if not self._lambda_vars:
            return None

        # COMMENT: We return the parents list starting from the second element ([1:]) to exclude the unnecessary lambda parameter
        lambda_var, *nested_name = self._lambda_vars[0].nested_element.parents

        if not nested_name:
            if len(self._lambda_vars) == 3 and len(n := self._lambda_vars[-1].nested_element.parents) == 2:
                return n[-1]

        self._nested_names = nested_name

        return lambda_var if not nested_name else nested_name[-1]

    def get_type_hint(self, type_model: Type) -> Type[Any]:
        def get_types(obj: Any):
            init_types = get_type_hints(obj.__init__) if hasattr(obj, "__init__") else {}
            annotations_types = get_type_hints(obj) if hasattr(obj, "__annotations__") else {}

            dict_types = init_types

            dict_types.update(annotations_types)
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

        # Means that we accessing the own class lambda x: x
        if len(nested_name) == 0:
            return type_model

        for var in nested_name:
            var_type_hint = current_type_hints[var]

            # It would be something like:   int | float | Decimal | ...
            if self.isUnionType(var_type_hint) or self.isOptional(var_type_hint):
                # For Union types, try to extract the non-None type
                return self.get_args(var_type_hint)

            current_instance_var = self.get_args(var_type_hint)

            # Handle Enum types - they don't have type hints like regular classes
            if isinstance(current_instance_var, type) and issubclass(current_instance_var, Enum):
                # For Enum types, we can't get further type hints, so return the Enum class itself
                if len(nested_name) == 1:  # If this is the last variable in the chain
                    return current_instance_var
                else:
                    # If there are more variables after an Enum, that's likely an error
                    raise TypeError(f"Cannot access nested properties on Enum type '{current_instance_var.__name__}'")

            if hasattr(current_instance_var, "dtype"):
                return current_instance_var.dtype

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
        # Handle Enum types first - they don't need unwrapping
        if isinstance(value, type) and issubclass(value, Enum):
            return value

        # Handle Optional types (Union[T, None])
        if cls.isOptional(value):
            args = get_args(value)
            # Return the first non-None type
            for arg in args:
                if arg is not type(None):
                    return arg
            return value

        # Handle other Union types (new Python 3.10+ syntax)
        if cls.isUnionType(value):
            args = get_args(value)
            # Return the first non-None type
            for arg in args:
                if arg is not type(None):
                    return arg
            return value

        return value

    @classmethod
    def extract_base_class(cls, type_hint: Any) -> Type[Any]:
        """
        Extracts the actual class type from a complex type annotation,
        removing generic wrappers like Literal, Union, List, Optional, etc.

        Args:
            type_hint: The type annotation to extract the class from

        Returns:
            The actual class type without generic wrappers

        Examples:
            >>> MemberInfo.extract_base_class(List[Person]) → Person
            >>> MemberInfo.extract_base_class(Optional[Person]) → Person
            >>> MemberInfo.extract_base_class(Union[Person, str]) → Person
            >>> MemberInfo.extract_base_class(Literal["admin", "user"]) → str
            >>> MemberInfo.extract_base_class(Optional[MyEnum]) → MyEnum
            >>> MemberInfo.extract_base_class(MyEnum) → MyEnum
        """
        # Handle None type
        if type_hint is None or type_hint is type(None):
            return type(None)

        # If it's already a regular class, return it
        if isinstance(type_hint, type) and not hasattr(type_hint, "__origin__"):
            return type_hint

        # Handle Enum types specifically
        if isinstance(type_hint, type) and issubclass(type_hint, Enum):
            return type_hint

        # Get the origin type (List, Union, Optional, etc.)
        origin = get_origin(type_hint)

        if origin is None:
            # No origin means it's likely a regular class
            return type_hint if isinstance(type_hint, type) else type(type_hint)

        # Get the arguments of the generic type
        args = get_args(type_hint)
        if not args:
            return origin

        # Handle common generic types
        if isinstance(origin, Iterable):
            # For List[SomeClass], extract SomeClass
            return cls.extract_base_class(args[0])

        elif cls.isOptional(type_hint) or cls.isUnionType(type_hint):
            # For Union types (including Optional), find the first non-None type
            non_none_types = [arg for arg in args if arg is not type(None)]
            if non_none_types:
                # If the first non-None type is an Enum, return it directly
                first_type = non_none_types[0]
                if isinstance(first_type, type) and issubclass(first_type, Enum):
                    return first_type
                return cls.extract_base_class(first_type)
            return type(None)

        elif hasattr(type_hint, "_name") and type_hint._name == "Literal":
            # For Literal types, return the type of the first literal value
            if args:
                return type(args[0])
            return str  # Default for empty Literal

        elif origin is tuple:
            # For Tuple[SomeClass, ...], extract the first type
            return cls.extract_base_class(args[0]) if args else tuple

        else:
            # For other generic types, try to extract the first argument
            # or return the origin type
            if args:
                return cls.extract_base_class(args[0])
            return origin

    @classmethod
    def get_property_class(cls, obj: Any) -> Type[Any]:
        """
        Extracts the actual class type from a complex type annotation using MemberInfo's get_args,
        removing generic wrappers like Literal, Union, List, Optional, etc.

        Args:
            obj: The type object to extract the class from

        Returns:
            The actual class type without generic wrappers
        """
        t_property = cls.get_args(obj)
        return cls.extract_base_class(t_property)
