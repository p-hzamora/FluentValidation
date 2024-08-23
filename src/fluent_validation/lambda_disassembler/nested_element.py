from typing import Iterable


class NestedElement[T]:
    def __init__(self, cond: T):
        self._cond: T = cond
        self._parent_list: list[str] = self._create_parent_list(cond)

    def __repr__(self) -> str:
        return f"{NestedElement.__name__}: {'.'.join(self._parent_list)}"

    @property
    def name(self) -> T:
        if self._parent_list:
            return self._parent_list[-1]
        else:
            return self._cond

    @property
    def parent(self) -> "NestedElement":
        if not self._parent_list:
            raise ValueError(f"Attribute '{self._cond}' has not parent values")
        new_cond = self._parent_list[:-1]
        return self.__get_parent(new_cond)

    @property
    def parents(self) -> list[T]:
        return self._parent_list

    def _create_parent_list(self, condition: T) -> Iterable[str]:
        if isinstance(condition, Iterable) and not isinstance(condition, str):
            return condition

        try:
            _list: list[str] = condition.split(".")

        except Exception:
            return []
        else:
            return _list

    @staticmethod
    def __get_parent(constructor: T) -> "NestedElement":
        return NestedElement[T](constructor)
