# from typing import Iterable, override

# from fluent_validation.validators import PropertyValidator
# from fluent_validation.IValidationContext import ValidationContext


# class EmptyValidator[T,TProperty](PropertyValidator[T,TProperty]):

# 	@override
# 	def is_valid(context:ValidationContext[T], value:TProperty)->bool:
# 		if (value is None):
# 			return True


# 		if isinstance(value, str) and (value.isspace()):
# 			return True


# 		if isinstance(value, Iterable) and (len(value) == 0):
# 			return True


# 		# return EqualityComparer<TProperty>.Default.Equals(value, default)


# 	@override
# 	def GetDefaultMessageTemplate(self, errorCode:str)->str:
# 		return self.Localized(errorCode, self.Name)


# 	def IsEmpty(enumerable:Iterable)->bool:
# 		var enumerator = enumerable.GetEnumerator()

# 		using (enumerator as IDisposable):
# 			return !enumerator.MoveNext()

