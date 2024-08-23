from abc import ABC, abstractmethod
import datetime
from decimal import Decimal
from enum import Enum
from typing import override


class Country:
    Name: str


class Payment:
    Amount: Decimal


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


class Address(IAddress):
    def __init__(
        self,
        Line1: str,
        Line2: str,
        Town: str,
        County: str,
        Postcode: str,
        Country: Country,
        Id: int,
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
    def __init__(self, Amount: Decimal, ProductName: str, Payments: list["Payment"]):
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
        NameField: str = None,
        Id: int = None,
        Surname: str = None,
        Forename: str = None,
        NickNames: str = None,
        DateOfBirth: datetime.datetime = None,
        Address: Address = None,
        Email: str = None,
        Discount: Decimal = None,
        Age: float = None,
        AnotherInt: int = None,
        CreditCard: str = None,
        Regex: str = None,
        min_length: int = None,
        max_length: int = None,
        Gender: EnumGender = None,
        Genderstr: str = None,
        Children: list["Person"] = [],
        Orders: list[Order] = [],
        NullableInt: int = None,
        NullableDiscount: Decimal = None,
        OtherNullableInt: int = None,
    ) -> None:
        self.Children: list[Person] = Children
        self.Orders: list[Order] = Orders
        self.NameField: str = NameField
        self.Id: int = Id
        self.Surname: str = Surname
        self.Forename: str = Forename
        self.Children: list["Person"] = Children
        self.NickNames: str = NickNames
        self.DateOfBirth: datetime.datetime = DateOfBirth
        self.NullableInt: int = NullableInt
        self.Address: Address = Address
        self.Orders: list[Order] = Orders
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
