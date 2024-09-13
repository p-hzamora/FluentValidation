from typing import Optional
from fluent_validation.validators.RangeValidator import IComparer


class IComparable[T]():

	def __init__(self, value:T	) -> None:
		self.value:T = value
	"""
	Summary:
			Compares the current instance with another object of the same type and returns
			an integer that indicates whether the current instance precedes, follows, or
			occurs in the same position in the sort order as the other object.

	Parameters:
	other:
			An object to compare with this instance.

	Returns:
			A value that indicates the relative order of the objects being compared. The
			return value has these meanings:

			Value – Meaning
			Less than zero – This instance precedes other in the sort order.
			Zero – This instance occurs in the same position in the sort order as other.

			Greater than zero – This instance follows other in the sort order.
	"""
	def CompareTo(self, other: Optional[T]) -> int: 
		if self.value < other:
			return -1
		elif self.value > other:
			return 1
		return 0
		


class ComparableComparer[T: IComparable[T]](IComparer[T]):
	@staticmethod
	def Compare(x: T, y: T) -> int:
		return IComparable(x).CompareTo(y)
