from datetime import datetime
from decimal import Decimal
from pathlib import Path
import sys
from typing import Optional

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "fluent_validation"].pop())

from dataclasses import dataclass  # noqa: E402
from src.fluent_validation.abstract_validator import AbstractValidator  # noqa: E402
from src.fluent_validation.enums import CascadeMode  # noqa: E402


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
    price: int = 200


class OrdersValidator(AbstractValidator[Orders]):
    def __init__(self) -> None:
        super().__init__()
        self.rule_for(lambda x: x.id).less_than_or_equal_to(100)
        self.rule_for(lambda x: x.name).not_equal("pablo")
        self.rule_for(lambda x: x.date).not_null()
        self.rule_for(lambda x: x.is_free).must(lambda x: isinstance(x, bool))
        self.rule_for(lambda x: x.price).less_than_or_equal_to(0).when(lambda x: x.is_free is True)


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


class PersonValidator(AbstractValidator[Person]):
    def __init__(self) -> None:
        super().__init__()
        self.ClassLevelCascadeMode = CascadeMode.Continue
        self.RuleLevelCascadeMode = CascadeMode.Continue
        self.rule_for(lambda x: x.name).Cascade(CascadeMode.Continue).not_null().not_empty().max_length(30)
        self.rule_for(lambda x: x.edad).not_null().must(lambda obj, value: obj.edad_min == value)
        self.rule_for(lambda x: x.fecha_ini).not_null().less_than_or_equal_to(lambda x: x.fecha_fin)
        self.rule_for(lambda x: x.edad).not_null().greater_than_or_equal_to(lambda x: x.edad_min).less_than_or_equal_to(lambda x: x.edad_max)
        self.rule_for(lambda x: x.ppto).not_null().must(lambda x: isinstance(x, (int, float, Decimal))).greater_than_or_equal_to(0)
        self.rule_for(lambda x: x.fecha_ini).not_null().less_than_or_equal_to(datetime.today())
        self.rule_for(lambda x: x.dni).not_null().must(lambda x: isinstance(x, str)).with_message("Custom message of IsInstance method").matches(RegexPattern.Dni)
        self.rule_for(lambda x: x.email).not_null().matches(RegexPattern.Email).with_message("The entered mail does not comply with the specific regex rules").max_length(15)
        # self.rule_for(lambda x: x.orders).set_validator(OrdersValidator())
        self.rule_for(lambda x: x.orders.name).not_equal("pablo")


# person = Person(
#     name="Pablo",
#     dni="00000000P",
#     email="pablo@gmail.org",
#     fecha_ini=datetime(2020, 11, 20),
#     fecha_fin=datetime.today(),
#     edad_min=5,
#     edad=5,
#     edad_max=20,
#     ppto=550,  # -550.56,
#     orders=Orders(150, "pablo", None, "SI", 10000),
# )

# validator = PersonValidator()
# result = validator.validate(person)


person = Person(
    name="",
    dni="___",
    email="pablo.org",
)

validator = PersonValidator()
validator.validate_and_throw(person)


print("\n" * 5)
result = validator.validate(
    person,
    lambda v: v.IncludeProperties(
        lambda x: x.name,
        lambda x: x.dni,
        lambda x: x.email,
    ),
)
if not result.is_valid:
    print(result.to_string())
