from fluent_validation.validators.RangeValidator import IComparer
from fluent_validation.validators.ComparableComparer import IComparable
from person import _Address as Address


class StreetNumberComparer(IComparer[Address]):
    def TryParseStreetNumber(self, s: str) -> bool:
        try:
            streetNumberStr = s.split(" ")[0]
            return True, int(streetNumberStr)
        except ValueError:
            return False, None

    def GetValue(self, o: object) -> int:
        if isinstance(o, Address):
            boolean, streetNumber = self.TryParseStreetNumber(o.Line1)
            if boolean:
                return streetNumber
        raise ValueError("Can't convert", o)

    def Compare(self, x: Address, y: Address) -> int:
        if x == y:
            return 0
        if x is None:
            return -1
        if y is None:
            return 1
        return IComparable(self.GetValue(x)).CompareTo(self.GetValue(y))
