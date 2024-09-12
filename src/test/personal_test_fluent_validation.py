from datetime import datetime
from decimal import Decimal
from pathlib import Path
import sys
from typing import Optional

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from dataclasses import dataclass  # noqa: E402
from fluent_validation.abstract_validator import AbstractValidator  # noqa: E402
from fluent_validation.enums import CascadeMode, Severity  # noqa: E402


class RegexPattern:
    Email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$"
    PhoneNumber = r"^\d{9}$"
    PostalCode = r"^\d{5}$"
    Dni = r"^[0-9]{8}[A-Z]$"


@dataclass
class Orders:
    id: Optional[int] = None
    name: str = None
    date: Optional[datetime] = None
    is_free: bool = False
    price: Decimal = 200
    credit_card: str = None


class OrdersValidator(AbstractValidator[Orders]):
    def __init__(self) -> None:
        super().__init__()
        self.rule_for(lambda x: x.id).less_than_or_equal_to(100)
        self.rule_for(lambda x: x.name).not_equal("pablo")
        self.rule_for(lambda x: x.date).not_null()
        self.rule_for(lambda x: x.is_free).must(lambda x: isinstance(x, bool))
        self.rule_for(lambda x: x.price).less_than_or_equal_to(Decimal("0.00")).when(lambda x: x.is_free is True).precision_scale(6, 2, True)  # max 9999.99
        self.rule_for(lambda o: o.credit_card).not_null().WithErrorCode("Null").not_empty().WithErrorCode("Empty").with_severity(Severity.Info).credit_card().with_severity(Severity.Warning)


@dataclass
class Person:
    name: str = None
    dni: str = None
    email: str = None
    edad: int = None
    fecha_fin: datetime = None
    fecha_ini: datetime = None
    person_id: int = None
    edad_min: int = None
    edad_max: int = None
    ppto: int | float | Decimal = None
    orders: list[Orders] = None


class PersonValidator(AbstractValidator[Person]):
    def __init__(self) -> None:
        super().__init__()
        self.ClassLevelCascadeMode = CascadeMode.Continue
        self.RuleLevelCascadeMode = CascadeMode.Continue
        self.rule_for(lambda x: x.name).Cascade(CascadeMode.Continue).not_null().not_empty().max_length(30)
        self.rule_for(lambda x: x.edad).Cascade(CascadeMode.Stop).not_null().must(lambda obj, value: obj.edad_min <= value <= obj.edad_max).with_severity(Severity.Warning)
        self.rule_for(lambda x: x.fecha_ini).not_null().less_than_or_equal_to(lambda x: x.fecha_fin)
        self.rule_for(lambda x: x.ppto).precision_scale(5, 2, True)
        self.rule_for(lambda x: x.fecha_ini).not_null().less_than_or_equal_to(datetime.today())
        self.rule_for(lambda x: x.dni).not_null().must(lambda x: isinstance(x, str)).with_message("Custom message of IsInstance method").matches(RegexPattern.Dni).with_name("DNI")
        self.rule_for(lambda x: x.email).not_null().matches(RegexPattern.Email).with_message("The entered mail does not comply with the specific regex rules").max_length(15)
        self.rule_for_each(lambda x: x.orders).set_validator(OrdersValidator())

        self.rule_set(
            "custom",
            lambda: (
                self.rule_for(lambda p: p.name).equal("pablo"),
                self.rule_for(lambda p: p.edad).equal(25),
                self.rule_for(lambda p: p.dni).equal("11111111P"),
            ),
        )


orders = [
    Orders(0, "pp", datetime.now(), True, Decimal("10000.00"), credit_card=""),
    Orders(50, "pablo", None, False, Decimal("10000.00"), credit_card=None),
    Orders(100, "luis", None, False, Decimal("10000.00"), credit_card="0000000000000000"),
    Orders(150, "Jhon", None, True, Decimal("10000.00"), credit_card="0000-1312-0000-1234"),
]

person_errors = Person(
    name="",
    dni="___",
    email="pablo.org",
    ppto=Decimal("12.558000000"),
    orders=orders,
)

person_correct = Person(
    name="Pablo",
    dni="51515151P",
    email="pp@hotmail.org",
    ppto=Decimal("12.55000000"),
    fecha_fin=datetime(2020, 11, 20),
    fecha_ini=datetime(2020, 11, 20),
    edad_min=1,
    edad_max=30,
    edad=31,
)

validator = PersonValidator()

result = validator.validate(
    person_errors,
    lambda v: (
        v.IncludeProperties(lambda x: x.orders),
        v.IncludeRuleSets("custom"),
    ),
)

if not result.is_valid:
    for err in result.errors:
        print(f"-- [{err.Severity}, {err.ErrorCode}]\t{err.PropertyName}: {err.ErrorMessage}")
print("OK")
