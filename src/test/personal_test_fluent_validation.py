from datetime import datetime
from decimal import Decimal
from pathlib import Path
import sys
from typing import Optional

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from dataclasses import dataclass  # noqa: E402
from fluent_validation.abstract_validator import AbstractValidator  # noqa: E402
from fluent_validation.enums import CascadeMode, Severity  # noqa: E402
from fluent_validation import IRuleBuilder, IRuleBuilderOptions


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
        super().__init__(Orders)
        self.rule_for(lambda x: x.id).less_than_or_equal_to(100)
        self.rule_for(lambda x: x.name).not_equal("pablo")
        self.rule_for(lambda x: x.date).not_null()
        self.rule_for(lambda x: x.is_free).must(lambda x: isinstance(x, bool))
        self.rule_for(lambda x: x.price).equal(Decimal("0.00")).when(lambda x: x.is_free is True).precision_scale(6, 2, True)  # max 9999.99
        self.rule_for(lambda o: o.credit_card).not_null().WithErrorCode("Notull").not_empty().WithErrorCode("Empty").with_severity(Severity.Info).credit_card().with_severity(Severity.Warning)


@dataclass
class Person:
    name: str = None
    dni: str = None
    email: str = None
    age: int = None
    deadline: datetime = None
    start_date: datetime = None
    person_id: int = None
    min_age: int = None
    max_age: int = None
    invoice: int | float | Decimal = None
    orders: list[Orders] = None


class PersonValidator(AbstractValidator[Person]):
    def __init__(self) -> None:
        super().__init__(Person)
        self.ClassLevelCascadeMode = CascadeMode.Continue
        self.RuleLevelCascadeMode = CascadeMode.Continue
        self.rule_for(lambda x: x.name).Cascade(CascadeMode.Continue).not_null().not_empty().max_length(30)
        self.rule_for(lambda x: x.age).Cascade(CascadeMode.Stop).not_null().must(lambda obj, value: obj.min_age <= value <= obj.max_age).with_severity(Severity.Warning)
        self.rule_for(lambda x: x.start_date).not_null().less_than_or_equal_to(lambda x: x.deadline)
        self.rule_for(lambda x: x.invoice).precision_scale(5, 2, True)
        self.rule_for(lambda x: x.start_date).not_null().less_than_or_equal_to(datetime.today())
        self.rule_for(lambda x: x.dni).not_null().must(lambda x: isinstance(x, str)).with_message("Custom message of IsInstance method").matches(RegexPattern.Dni).with_name("DNI")
        self.rule_for(lambda x: x.email).not_null().matches(RegexPattern.Email).with_message("The entered mail does not comply with the specific regex rules").max_length(15)
        self.rule_for_each(lambda x: x.orders).set_validator(OrdersValidator())

        self.rule_set(
            "custom",
            lambda: (
                self.rule_for(lambda p: p.name).equal("pablo"),
                self.rule_for(lambda p: p.age).equal(25),
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
    invoice=Decimal("12.558000000"),
    orders=orders,
)

person_correct = Person(
    name="Pablo",
    dni="51515151P",
    email="pp@hotmail.org",
    invoice=Decimal("12.55000000"),
    deadline=datetime(2020, 11, 20),
    start_date=datetime(2020, 11, 20),
    min_age=1,
    max_age=30,
    age=31,
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


# Custom Validators
@dataclass
class Pet:
    age: Optional[int] = None
    name: Optional[str] = None


class Person:
    def __init__(self, pet: Optional[list[Pet]] = None):
        self.Pets: list[Pet] = pet if pet is not None else []


class MyCustomValidators:
    def ListMustContainFewerThan[T, TElement](ruleBuilder: IRuleBuilder[T, list[TElement]], num: int) -> IRuleBuilderOptions[T, list[TElement]]:
        return ruleBuilder.must(
            lambda rootObject, list_, context: (
                context.MessageFormatter.AppendArgument("MaxElements", num).AppendArgument("TotalElements", len(list_)),
                len(list_) < num,
            )[1]
        ).with_message("{PropertyName} must contain fewer than {MaxElements} items. The list contains {TotalElements} element")

    IRuleBuilder.ListMustContainFewerThan = ListMustContainFewerThan


class PersonValidator(AbstractValidator[Person], MyCustomValidators):
    def __init__(self) -> None:
        super().__init__(Person)
        self.rule_for(lambda x: x.Pets).ListMustContainFewerThan(10).must(lambda x: len(x) == 10).with_severity(Severity.Warning)


person = Person(
    [
        Pet(),
        Pet(),
        Pet(),
        Pet(),
        Pet(),
        Pet(),
        Pet(),
        Pet(),
        Pet(),
        Pet(),
        Pet(),
    ]
)
validator = PersonValidator().validate_and_throw(person)
