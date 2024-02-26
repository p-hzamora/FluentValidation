from datetime import datetime
from decimal import Decimal
from pathlib import Path
import sys

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "FluentValidation"].pop())

from dataclasses import dataclass  # noqa: E402
from src.FluentValidation.abstract_validator import AbstractValidator  # noqa: E402
from src.FluentValidation.enums import CascadeMode  # noqa: E402


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
        self.RuleFor(lambda x: x.edad).Must(lambda obj, value: obj.edad_min == value)
        self.RuleFor(lambda x: x.fecha_ini).LessThanOrEqualTo(lambda x: x.fecha_fin)
        self.RuleFor(lambda x: x.edad).GreaterThanOrEqualTo(lambda x: x.edad_min).LessThanOrEqualTo(lambda x: x.edad_max)

        self.RuleFor(lambda x: x.ppto).Must(lambda x: isinstance(x, (int, float, Decimal))).GreaterThanOrEqualTo(0)

        self.RuleFor(lambda x: x.fecha_ini).LessThanOrEqualTo(datetime.today())

        self.RuleFor(lambda x: x.dni).Must(lambda x: isinstance(x, str)).WithMessage("Custom message of IsInstance method").Matches(RegexPattern.Dni)

        self.RuleFor(lambda x: x.email).NotNull().Matches(RegexPattern.Email).WithMessage("The entered mail does not comply with the specific regex rules").MaxLength(15)


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
