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

from __future__ import annotations
from typing import Iterable, Optional, override, Callable, Any, TYPE_CHECKING
import re

from fluent_validation.MemberInfo import MemberInfo
from fluent_validation.internal.IValidatorSelector import IValidatorSelector


if TYPE_CHECKING:
    from fluent_validation.IValidationRule import IValidationRule
    from fluent_validation.IValidationContext import IValidationContext


class MemberNameValidatorSelector(IValidatorSelector):
    DisableCascadeKey: str = "_FV_DisableSelectorCascadeForChildRules"

    _collectionIndexNormalizer: re.Pattern[str] = re.compile(r"\[.*?\]")

    def __init__(self, memberNames: Iterable[str]):
        self._memberNames: Iterable[str] = memberNames

    @property
    def MemberNames(self) -> Iterable[str]:
        return self._memberNames

    @override
    def CanExecute(self, rule: IValidationRule, propertyPath: str, context: IValidationContext) -> bool:
        from fluent_validation.internal.IncludeRule import IIncludeRule

        # Validator selector only applies to the top level.
        # If we're running in a child context then this means that the child validator has already been selected
        # Because of this, we assume that the rule should continue (ie if the parent rule is valid, all children are valid)
        isChildContext: bool = context.IsChildContext
        cascadeEnabled: bool = self.DisableCascadeKey not in context.RootContextData

        # If a child validator is being executed and the cascade is enabled (which is the default)
        # then the child validator's rule should always be included.
        # The only time this isn't the case is if the member names contained for inclusion are for child
        # properties (which is indicated by them containing a period).
        if isChildContext and cascadeEnabled and not any(["." in x for x in self._memberNames]):
            return True

        if isinstance(rule, IIncludeRule):
            return True
        # Stores the normalized property name if we're working with collection properties
        # eg Orders[0].Name -> Orders[].Name. This is only initialized if needed (see below).
        normalizedPropertyPath: Optional[str] = None

        # If the current property path is equal to any of the member names for inclusion
        # or it's a child property path (indicated by a period) where we have a partial match.
        for memberName in self._memberNames:
            # If the property path is equal to any of the input member names then it should be executed.
            if memberName == propertyPath:
                return True

            # If the property path is for a child property,
            # and the parent property is selected for inclusion,
            # then it should be allowed to execute.
            if propertyPath.startswith(memberName + "."):
                return True

            # If the property path is for a parent property,
            # and any of its child properties are selected for inclusion
            # then it should be allowed to execute
            if memberName.startswith(propertyPath + "."):
                return True

            # If the property path is for a collection property
            # and a child property for this collection has been passed in for inclusion.
            # For example, memberName is "Orders[0].Amount"
            # and propertyPath is "Orders" then it should be allowed to execute.
            if memberName.startswith(propertyPath + "["):
                return True

            # If property path is for child property within collection,
            # and member path contains wildcard [] then this means that we want to match
            # with all items in the collection, but we need to normalize the property path
            # in order to match. For example, if the propertyPath is "Orders[0].Name"
            # and the memberName for inclusion is "Orders[].Name" then this should
            # be allowed to match.
            if "[]" in memberName:
                if normalizedPropertyPath is None:
                    # Normalize the property path using a regex. Orders[0].Name -> Orders[].Name.
                    normalizedPropertyPath = self._collectionIndexNormalizer.sub("[]", propertyPath)

                if memberName == normalizedPropertyPath:
                    return True

                if memberName.startswith(normalizedPropertyPath + "."):
                    return True

                if memberName.startswith(normalizedPropertyPath + "["):
                    return True

        return False

    # TODOL: Check if it correct 	public static string[] MemberNamesFromExpressions<T>(params Expression<Func<T, object>>[] propertyExpressions) {

    @classmethod
    def MemberNamesFromExpressions[T](cls, *propertyExpressions: Callable[[T], Any]) -> list[str]:
        """Gets member names from expressions"""
        members: list[str] = [cls.MemberFromExpression(x) for x in propertyExpressions]
        return members

    @staticmethod
    def MemberFromExpression[T](expression: Callable[[T], Any]) -> str:
        from fluent_validation.ValidatorOptions import ValidatorOptions

        # get list of all values in expression (one is expected) and get first
        propertyName = ValidatorOptions.Global.PropertyNameResolver(type(T), MemberInfo(expression), expression)

        if not propertyName:
            raise ValueError(f"Expression '{expression}' does not specify a valid property or field.")

        return propertyName
