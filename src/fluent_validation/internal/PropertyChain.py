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
from typing import Callable, Iterable, Any, Optional, override

from fluent_validation.MemberInfo import MemberInfo
from fluent_validation.ValidatorOptions import ValidatorOptions


class PropertyChain:
    def __init__(self, parent: Optional["PropertyChain"] = None, memberNames: Optional[Iterable[str]] = None):
        self._memberNames: list[str] = []

        if parent and not memberNames and len(parent._memberNames) > 0:
            self._memberNames.extend(parent._memberNames)
        elif not parent and memberNames:
            self._memberNames.extend(memberNames)

    # Original method
    # @staticmethod
    # def FromExpression(expression:Callable[...,Any])->"PropertyChain":
    # 	memberName:list[str] = []

    # 	getMemberExp = new Func<Expression, MemberExpression>(toUnwrap => {
    # 		if (toUnwrap is UnaryExpression:
    # 			return ((UnaryExpression)toUnwrap).Operand as MemberExpression

    # 		return toUnwrap as MemberExpression)

    # 	memberExp = getMemberExp(expression.Body)

    # 	while(memberExp != null:
    # 		memberNames.Push(memberExp.Member.Name)
    # 		memberExp = getMemberExp(memberExp.Expression)

    # 	return new PropertyChain(memberNames)

    @staticmethod
    def FromExpression(expression: Callable[..., Any]) -> PropertyChain:
        """Creates a PropertyChain from a lambda expression"""
        # COMMENT: TreeInstruction().to_list() returns a list depending on the number of attributes the lambda has.
        #  Since we always pass one attr, we only need to access the first position of the list if not empty
        member_info = MemberInfo(expression)

        name = member_info.Name
        nested_names = member_info.NestedNames
        if not name:
            # FIXME [x]: Checked who to resovle with original code
            return PropertyChain(None, [])

        if not nested_names:
            return PropertyChain(None, [name])
        return PropertyChain(None, nested_names)

    # TODOM: Checked if the MemberInfo class from C# is registering the same value in python using __class__.__name__
    def Add(self, member: MemberInfo) -> None:
        if isinstance(member, str):
            if not (member is None or member == ""):
                self._memberNames.append(member)
            return None
        if member:
            self._memberNames.append(member.Name)
        return None

    def AddIndexer(self, indexer: Any, surroundWithBrackets: bool = True) -> None:
        if len(self._memberNames) == 0:
            raise AttributeError("Could not apply an Indexer because the property chain is empty.")

        last: str = self._memberNames[len(self._memberNames) - 1]
        last += f"[{indexer}]" if surroundWithBrackets else indexer

        self._memberNames[len(self._memberNames) - 1] = last
        return None

    @override
    def ToString(self) -> str:
        match len(self._memberNames):
            case 0:
                return ""
            case 1:
                return self._memberNames[0]
            case _:
                return ValidatorOptions.Global.PropertyChainSeparator.join(self._memberNames)

    # bool IsChildChainOf(PropertyChain parentChain:
    # 	return ToString().StartsWith(parentChain.ToString())

    # [Obsolete("BuildPropertyName is deprecated due to its misleading name. Use BuildPropertyPath instead which does the same thing.")]
    # string BuildPropertyName(string propertyName)
    # 	=> BuildPropertyPath(propertyName)

    def BuildPropertyPath(self, propertyName: str) -> str:
        if len(self._memberNames) == 0:
            return propertyName

        chain = PropertyChain(self)
        chain.Add(propertyName)
        return chain.ToString()

    @property
    def Count(self) -> int:
        return len(self._memberNames)

    def __len__(self):
        return len(self._memberNames)
