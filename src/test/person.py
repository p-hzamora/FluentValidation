from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, override


@dataclass
class Country:
    Name: str = None


@dataclass
class Payment:
    Amount: Decimal = Decimal("0.00")


class EnumGender(Enum):
    Female = 1
    Male = 2


class IAddress(ABC):
    @property
    @abstractmethod
    def Line1(self) -> str: ...

    @property
    @abstractmethod
    def Line2(self) -> str: ...

    @property
    @abstractmethod
    def Town(self) -> str: ...

    @property
    @abstractmethod
    def County(self) -> str: ...

    @property
    @abstractmethod
    def Postcode(self) -> str: ...

    @property
    @abstractmethod
    def Country(self) -> Country: ...


class _Address(IAddress):
    def __init__(
        self,
        Line1: str = None,
        Line2: str = None,
        Town: str = None,
        County: str = None,
        Postcode: str = None,
        Country: Country = None,
        Id: int = 0,
    ):
        self._Line1: str = Line1
        self._Line2: str = Line2
        self._Town: str = Town
        self._County: str = County
        self._Postcode: str = Postcode
        self._Country: Country = Country
        self._Id: int = Id

    @override
    @property
    def Line1(self) -> str:
        return self._Line1

    @override
    @property
    def Line2(self) -> str:
        return self._Line2

    @override
    @property
    def Town(self) -> str:
        return self._Town

    @override
    @property
    def County(self) -> str:
        return self._County

    @override
    @property
    def Postcode(self) -> str:
        return self._Postcode

    @override
    @property
    def Country(self) -> Country:
        return self._Country

    @override
    @property
    def Id(self) -> int:
        return self._Id


class IOrder(ABC):
    @property
    @abstractmethod
    def Amount(self) -> Decimal: ...


class Order(IOrder):
    def __init__(
        self,
        Amount: Decimal = Decimal("0"),
        ProductName: str = None,
        Payments: list["Payment"] = None,
    ):
        self._Amount: Decimal = Amount
        self._ProductName: str = ProductName
        self._Payments: list["Payment"] = Payments

    @property
    def ProductName(self) -> str:
        return self._ProductName

    @property
    def Amount(self) -> Decimal:
        return self._Amount

    @property
    def Payments(self) -> list["Payment"]:
        return self._Payments


class Person:
    def __init__(
        self,
        NameField: Optional[str] = None,
        Id: int = 0,
        Surname: Optional[str] = None,
        Forename: Optional[str] = None,
        NickNames: Optional[list[str]] = None,
        DateOfBirth: Optional[datetime.datetime] = None,
        Address: Optional[_Address] = None,
        Email: Optional[str] = None,
        Discount: Optional[Decimal] = None,
        Age: Optional[float] = None,
        AnotherInt: int = 0,
        CreditCard: Optional[str] = None,
        Regex: Optional[str] = None,
        min_length: int = 0,
        max_length: int = 0,
        Gender: Optional[EnumGender] = None,
        Genderstr: Optional[str] = None,
        Children: list[Optional["Person"]] = [],
        Orders: list[Optional[Order]] = [],
        NullableInt: Optional[int] = None,
        NullableDiscount: Optional[Decimal] = None,
        OtherNullableInt: Optional[int] = None,
    ) -> None:
        self.Children: list[Person] = Children
        self.Orders: list[Order] = Orders
        self.NameField: str = NameField
        self.Id: int = Id
        self.Surname: str = Surname
        self.Forename: str = Forename
        self.NickNames: list[str] = NickNames
        self.DateOfBirth: datetime.datetime = DateOfBirth
        self.NullableInt: int = NullableInt
        self.Address: _Address = Address
        self.Email: str = Email
        self.Discount: Decimal = Discount
        self.NullableDiscount: Decimal = NullableDiscount
        self.Age: float = Age
        self.AnotherInt: int = AnotherInt
        self.CreditCard: str = CreditCard
        self.OtherNullableInt: int = OtherNullableInt
        self.Regex: str = Regex
        self.min_length: int = min_length
        self.max_length: int = max_length
        self.Gender: EnumGender = Gender
        self.Genderstr: str = Genderstr

    @staticmethod
    def CalculateSalary() -> int:
        return 20

    @property
    def ForenameReadOnly(self) -> str:
        return self.Forename
