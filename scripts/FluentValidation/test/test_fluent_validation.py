from datetime import datetime
from decimal import Decimal
from pathlib import Path
import sys

sys.path.append(
    [str(x) for x in Path(__file__).parents if x.name == "FluentValidation"].pop()
)

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
        self.ClassLevelCascadeMode = CascadeMode.Stop
        self.RuleLevelCascadeMode = CascadeMode.Stop
        self.RuleFor(lambda x: x.fecha_ini).IsInstance(int).WithMessage("asdf").GreaterThanOrEqual(lambda x: x.fecha_fin)
        self.RuleFor(lambda x: x.edad).GreaterThanOrEqual(lambda x: x.edad_min).LessThanOrEqual(lambda x: x.edad_max)
        self.RuleFor(lambda x: x.ppto).IsInstance(int | float | Decimal).GreaterThanOrEqual(0)
        self.RuleFor(lambda x: x.fecha_ini).GreaterThan(datetime.today())
        self.RuleFor(lambda x: x.dni).IsInstance(float).WithMessage("mensaje personalizado de is_instance").Matches(RegexPattern.PhoneNumber).Length(10, 50).WithMessage("no tiene los caracteres exactos"
        ).Length(15, 20).WithMessage("error personalizado de longitud")

        self.RuleFor(lambda x: x.email).NotNull().MaxLength(5).Matches(RegexPattern.Email).WithMessage("El correo introducido no cumple con la regex especifica"
        ).MaxLength(5).WithMessage("El correo excede los 5 caracteres")
        pass


person = Person(
    name="Pablo",
    dni="51527736P",
    email="pablogmail.org",
    fecha_ini=datetime(2020, 11, 20),
    fecha_fin=datetime.today(),
    edad_min=5,
    edad=4,
    edad_max=20,
    ppto="550",  # -550.56
)


validator = PersonValidator()
result = validator.validate(person)
if not result.is_valid:
    for error in result.errors:
        print(f"Error en '{error.PropertyName}' con mensaje:{error.ErrorMessage}")
