from typing import Any, Callable, NamedTuple
import unittest
import sys
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation.abstract_validator import AbstractValidator
from fluent_validation.InlineValidator import InlineValidator

from person import IOrder, Order, Person
from TestValidator import TestValidator


class NamedTupleTest(NamedTuple):
    Item1: Person
    Item2: Any


class CollectionValidatorWithParentTests(unittest.TestCase):
    def setUp(self):
        self.person: Person = Person(
            AnotherInt=99,
            Children=[Person(Email="person@email.com")],
            Orders=[
                Order(ProductName="email_that_does_not_belong_to_a_person", Amount=99),
                Order(ProductName="person@email.com", Amount=1),
                Order(ProductName="another_email_that_does_not_belong_to_a_person", Amount=1),
            ],
        )

    def test_Validates_collection(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Surname).not_null(),
            lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(
                lambda y: OrderValidator(y),
            ),
        )

        results = validator.validate(self.person)
        self.assertEqual(len(results.errors), 3)

        self.assertEqual(results.errors[0].PropertyName, "Surname")
        self.assertEqual(results.errors[1].PropertyName, "Orders[0].ProductName")
        self.assertEqual(results.errors[2].PropertyName, "Orders[2].ProductName")

    # async def test_Validates_collection_asynchronously(self):
    # 	validator = TestValidator(
    # 		lambda v: v.rule_for(lambda x: x.Surname).not_null(),
    # 		lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(lambda y: AsyncOrderValidator(y))
    # 	)

    # 	results = await validator.ValidateAsync(self.person)
    # 	self.assertEqual(len(results.errors),3)

    # 	self.assertEqual(results.errors[1].PropertyName,"Orders[0].ProductName")
    # 	self.assertEqual(results.errors[2].PropertyName,"Orders[2].ProductName")

    def test_Validates_collection_several_levels_deep(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Surname).not_null(),
            lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(lambda y: OrderValidator(y)),
        )

        rootValidator = InlineValidator[NamedTupleTest[Person, Any]](NamedTupleTest[Person, Any])
        rootValidator.rule_for(lambda x: x.Item1).set_validator(validator)

        # FIXME [x]: We need to resolve event loop to propagate the values throw the conditions properly
        results = rootValidator.validate(NamedTupleTest(self.person, object()))
        self.assertEqual(len(results.errors), 3)

        self.assertEqual(results.errors[1].PropertyName, "Item1.Orders[0].ProductName")
        self.assertEqual(results.errors[2].PropertyName, "Item1.Orders[2].ProductName")

    # async def test_Validates_collection_several_levels_deep_async(self):
    # 	validator = TestValidator(
    # 		lambda v: v.rule_for(lambda x: x.Surname).not_null(),
    # 		lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(lambda y: OrderValidator(y))
    # 	)

    # 	rootValidator = InlineValidator[NamedTupleTest[Person, Any]](NamedTupleTest[Person, Any])
    # 	rootValidator.rule_for(lambda x: x.Item1).set_validator(validator)

    # 	results  = await rootValidator.ValidateAsync(NamedTupleTest(self.person, object()))
    # 	self.assertEqual(len(results.errors),3)

    # 	self.assertEqual(results.errors[1].PropertyName,"Item1.Orders[0].ProductName")
    # 	self.assertEqual(results.errors[2].PropertyName,"Item1.Orders[2].ProductName")

    def test_Collection_should_be_explicitly_included_with_expression(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Surname).not_null(),
            lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(
                lambda y: OrderValidator(y),
            ),
        )

        results = validator.validate(self.person, lambda v: v.IncludeProperties(lambda x: x.Orders))
        self.assertEqual(len(results.errors), 2)

    def test_Collection_should_be_explicitly_included_with_string(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Surname).not_null(),
            lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(
                lambda y: OrderValidator(y),
            ),
        )

        results = validator.validate(self.person, lambda v: v.IncludeProperties("Orders"))
        self.assertEqual(len(results.errors), 2)

    def test_Collection_should_be_excluded(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Surname).not_null(),
            lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(
                lambda y: OrderValidator(y),
            ),
        )

        results = validator.validate(self.person, lambda v: v.IncludeProperties(lambda x: x.Forename))
        self.assertEqual(len(results.errors), 0)

    def test_Condition_should_work_with_child_collection(self):
        validator = TestValidator(
            lambda v: v.rule_for_each(lambda x: x.Orders)
            .set_validator(lambda y: OrderValidator(y))
            .when(
                lambda x: len(x.Orders) == 4  # there are only 3
            ),
        )

        result = validator.validate(self.person)
        self.assertTrue(result.is_valid)

    # async def test_Async_condition_should_work_with_child_collection(self):
    # 	validator = TestValidator(
    # 		lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(lambda y: OrderValidator(y)).WhenAsync((x, c) => Task.FromResult(x.Orders.Count == 4) # there are only 3
    # 	)

    # 	result = await validator.ValidateAsync(self.person)
    # 	self.assertTrue(result.is_valid)

    def test_Skips_null_items(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null(), lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(lambda y: OrderValidator(y)))

        self.person.Orders[0] = None
        results = validator.validate(self.person)
        self.assertEqual(len(results.errors), 2)  # 2 errors - 1 for person, 1 for 3rd Order.

    def test_Can_validate_collection_using_validator_for_base_type(self):
        validator = TestValidator(lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(lambda y: OrderInterfaceValidator(y)))

        result = validator.validate(self.person)
        self.assertFalse(result.is_valid)

    def test_Can_specify_condition_for_individual_collection_elements(self):
        validator = TestValidator(
            lambda v: v.rule_for_each(lambda x: x.Orders)
            .where(lambda x: x.Amount != 1)
            .set_validator(
                lambda y: OrderValidator(y),
            )
        )

        results = validator.validate(self.person)
        self.assertEqual(len(results.errors), 1)

    def test_Should_override_property_name(self):
        validator = TestValidator(lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(lambda y: OrderValidator(y)).override_property_name("Orders2"))

        results = validator.validate(self.person)
        self.assertEqual(results.errors[0].PropertyName, "Orders2[0].ProductName")

    def test_Should_work_with_top_level_collection_validator(self):
        personValidator = InlineValidator[Person](Person)
        personValidator.rule_for(lambda x: x.Surname).not_null()

        validator = InlineValidator[list[Person]](list[Person])
        validator.rule_for_each(lambda x: x).set_validator(personValidator)

        results = validator.validate([Person(), Person(), Person(Surname="Bishop")])
        self.assertEqual(len(results.errors), 2)
        self.assertEqual(results.errors[0].PropertyName, "x[0].Surname")

    def test_Should_work_with_top_level_collection_validator_and_overriden_name(self):
        personValidator = InlineValidator[Person](Person)
        personValidator.rule_for(lambda x: x.Surname).not_null()

        validator = InlineValidator[list[Person]](list[Person])
        validator.rule_for_each(lambda x: x).set_validator(personValidator).override_property_name("test")

        results = validator.validate([Person(), Person(), Person(Surname="Bishop")])
        self.assertEqual(len(results.errors), 2)
        self.assertEqual(results.errors[0].PropertyName, "test[0].Surname")

    def test_Creates_validator_using_context_from_property_value(self):
        personValidator = InlineValidator[Person](Person)

        normalOrderValidator = InlineValidator[Order](Order)
        normalOrderValidator.rule_for(lambda x: x.Amount).greater_than(0)

        freeOrderValidator = InlineValidator[Order](Order)
        freeOrderValidator.rule_for(lambda x: x.Amount).equal(0)

        personValidator.rule_for_each(lambda x: x.Orders).set_validator(lambda p, order: freeOrderValidator if order.ProductName == "FreeProduct" else normalOrderValidator)

        result1 = personValidator.validate(Person(Orders=[Order(ProductName="FreeProduct")]))
        self.assertTrue(result1.is_valid)

        result2 = personValidator.validate(Person(Orders=[Order()]))
        self.assertFalse(result2.is_valid)
        self.assertEqual(result2.errors[0].ErrorCode, "GreaterThanValidator")


class OrderValidator(AbstractValidator[Order]):
    def __init__(self, person: Person) -> None:
        super().__init__(Order)
        self.rule_for(lambda x: x.ProductName).must(self.BeOneOfTheChildrensEmailAddress(person))

    @staticmethod
    def BeOneOfTheChildrensEmailAddress(person: Person) -> Callable[[str], bool]:
        return lambda productName: any(child.Email == productName for child in person.Children)


class OrderInterfaceValidator(AbstractValidator[IOrder]):
    def __init__(self, person: Person) -> None:
        super().__init__(IOrder)
        self.rule_for(lambda x: x.Amount).not_equal(person.AnotherInt)


# class AsyncOrderValidator(AbstractValidator[Order]):
# 	def __init__(self,person:Person) -> None:
# 		super().__init__()
# 		self.rule_for(lambda x: x.ProductName).MustAsync(self.BeOneOfTheChildrensEmailAddress(person))

# 	private Func[string, CancellationToken, Task[bool]] BeOneOfTheChildrensEmailAddress(Person person) {
# 		return (productName, cancel) => Task.FromResult(self.person.Children.Any(lambda child: child.Email == productName))
# 	)
# )

if __name__ == "__main__":
    unittest.main()
