from typing import Callable, Optional
from fluent_validation.MemberInfo import MemberInfo


class AccessorCache[T]:
    _cache = {}

    @staticmethod
    def GetCachedAccessor[TProperty](member: Optional[MemberInfo], expression: Callable[[T], TProperty], bypass_cache: bool = False, cache_prefix=None) -> Callable[[T], TProperty]:
        if bypass_cache:
            return expression

        if member is None:
            if isinstance(expression, str):  # Python equivalent to "ParameterExpression"
                key = Key(None, expression, f"{type(expression).__name__}:{cache_prefix}")
            else:
                return expression
        else:
            key = Key(member, expression, cache_prefix)

        if key not in AccessorCache._cache:
            AccessorCache._cache[key] = expression

        return AccessorCache._cache[key]

    @staticmethod
    def clear():
        AccessorCache._cache.clear()


class Key:
    def __init__(self, member: MemberInfo, expression, cache_prefix):
        self._member_info = member
        self._expression_debug_view = f"{cache_prefix}{expression}" if cache_prefix else str(expression)

    def __eq__(self, other):
        if not isinstance(other, Key):
            return False
        return self._member_info == other._member_info and self._expression_debug_view == other._expression_debug_view

    def __hash__(self):
        # Python equivalent to GetHashCode() with some custom hash calculation
        hash_member_info = hash(self._member_info) if self._member_info is not None else 0
        hash_expression_debug_view = hash(self._expression_debug_view) if self._expression_debug_view is not None else 0

        # Combining the hashes similar to the C# approach
        return (hash_member_info * 397) ^ hash_expression_debug_view
