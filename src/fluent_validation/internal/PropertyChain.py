from typing import Callable, Iterable, Any, Optional, override

from fluent_validation.MemberInfo import MemberInfo
from fluent_validation.ValidatorOptions import ValidatorOptions
from fluent_validation.lambda_disassembler.tree_instruction import TreeInstruction


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
    def FromExpression(expression: Callable[..., Any]) -> "PropertyChain":
        # COMMENT: TreeInstruction().to_list() returns a list depending on the number of attributes the lambda has. Since we always pass one attr, we only need to access the first position of the list
        memberNames = TreeInstruction(expression).to_list()
        if not memberNames:
            # FIXME [ ]: Checked who to resovle with original code
            raise ValueError
            return None

        # COMMENT: We return the parents list starting from the second element ([1:]) to exclude the unnecessary lambda parameter
        var, *memberNames = memberNames[0].nested_element.parents
        if not memberNames:
            return PropertyChain(None, var)
        return PropertyChain(None, memberNames)

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
