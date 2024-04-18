from datetime import datetime
from decimal import Decimal
from pathlib import Path
import sys

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from dataclasses import dataclass  # noqa: E402
from FluentValidation.abstract_validator import AbstractValidator  # noqa: E402
from FluentValidation.enums import CascadeMode  # noqa: E402


class RegexPattern:
    Email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$"
    PhoneNumber = r"^\d{9}$"
    PostalCode = r"^\d{5}$"
    Dni = r"^[0-9]{8}[A-Z]$"


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
        self.rule_for(lambda x: x.edad).must(lambda obj, value: obj.edad_min == value)
        self.rule_for(lambda x: x.fecha_ini).less_than_or_equal_to(lambda x: x.fecha_fin)
        self.rule_for(lambda x: x.edad).greater_than_or_equal_to(lambda x: x.edad_min).less_than_or_equal_to(lambda x: x.edad_max)

        self.rule_for(lambda x: x.ppto).must(lambda x: isinstance(x, (int, float, Decimal))).greater_than_or_equal_to(0)

        self.rule_for(lambda x: x.fecha_ini).less_than_or_equal_to(datetime.today())

        self.rule_for(lambda x: x.dni).must(lambda x: isinstance(x, str)).with_message("Custom message of IsInstance method").matches(RegexPattern.Dni)

        self.rule_for(lambda x: x.email).not_null().matches(RegexPattern.Email).with_message("The entered mail does not comply with the specific regex rules").max_length(15)


person = Person(
    name="Pablo",
    dni="00000000P",
    email="pablo@gmail.org",
    fecha_ini=datetime(2020, 11, 20),
    fecha_fin=datetime.today(),
    edad_min=5,
    edad=5,
    edad_max=20,
    ppto=550,  # -550.56
)


validator = PersonValidator()
result = validator.validate(person)
if not result.is_valid:
    for error in result.errors:
        print(f"Error en '{error.PropertyName}' con error {error.ErrorCode} y mensaje: {error.ErrorMessage}")
