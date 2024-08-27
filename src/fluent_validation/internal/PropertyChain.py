from typing import Iterable, Any, Optional, override

from src.fluent_validation.ValidatorOptions import ValidatorOptions


class PropertyChain:
    def __init__(self, parent: Optional["PropertyChain"] = None, memberNames: Optional[Iterable[str]] = None):
        self._memberNames: list[str] = []

        if parent and not memberNames and len(parent._memberNames) > 0:
            self._memberNames.extend(parent._memberNames)
        elif not parent and memberNames:
            self._memberNames.extend(memberNames)

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

    # TODOM: Checked if the MemberInfo class from C# is registering the same value in python using __class__.__name__
    def Add(self, member: Any) -> None:
        if isinstance(member, str):
            if not (member is None or member == ""):
                self._memberNames.append(member)
                return None
        if member:
            self._memberNames.append(member.__class__.__name__)
        return None

    # def AddIndexer(self, object indexer, bool surroundWithBrackets = true->None:
    # 	if self._memberNames.Count == 0:
    # 		throw new InvalidOperationException("Could not apply an Indexer because the property chain is empty.")

    # 	string last = self._memberNames[self._memberNames.Count - 1]
    # 	last += surroundWithBrackets ? "[" + indexer + "]" : indexer

    # 	self._memberNames[self._memberNames.Count - 1] = last

    @override
    def ToString(self)->str:
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

    def BuildPropertyPath(self, propertyName:str)->str:
        if len(self._memberNames) == 0:
            return propertyName

        chain = PropertyChain(self)
        chain.Add(propertyName)
        return chain.ToString()

    @property
    def Count(self)->int:
        return len(self._memberNames)
