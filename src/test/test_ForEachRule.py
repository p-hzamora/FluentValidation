import sys
from typing import Any
import unittest
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "fluent_validation"].pop())

from src.fluent_validation.InlineValidator import InlineValidator
from src.fluent_validation.IValidationContext import ValidationContext
from src.fluent_validation.abstract_validator import AbstractValidator
from src.fluent_validation.validators.NotNullValidator import NotNullValidator
from src.fluent_validation.validators.IpropertyValidator import IAsyncPropertyValidator, IPropertyValidator
from TestValidator import TestValidator  # noqa: E402
from person import IOrder, Person, Order  # noqa: E402


class Request:
    person: Person = None


class MyAsyncNotNullValidator[T, TProperty](IAsyncPropertyValidator[T, TProperty]):
    def __init__(self) -> None:
        super().__init__()
        self._inner: IPropertyValidator[T, TProperty] = NotNullValidator[T, TProperty]()

    async def IsValidAsync(self, context: ValidationContext[T], value: TProperty):  # , CancellationToken cancellation
        return await self._inner.is_valid(context, value)

    @property
    def Name(self) -> str:
        return self._inner.Name

    def GetDefaultMessageTemplate(self, errorCode: str) -> str:
        return self._inner.get_default_message_template(errorCode)


class ForEachRuleTests(unittest.TestCase):
    _lock: Any = object()

    def setUp(self) -> None:
        self._counter: int = 0

        self._person: Person = Person(
            Orders=[
                Order(Amount=5),
                Order(ProductName="Foo"),
            ]
        )

    def test_Executes_rule_for_each_item_in_collection(self):
        validator = TestValidator(lambda v: v.rule_for_each(lambda x: x.NickNames).not_null())

        person = Person(NickNames=[None, "foo", None])

        result = validator.validate(person)
        self.assertEqual(len(result.errors), 2)

    def test_Correctly_gets_collection_indices(self):
        validator = TestValidator(lambda v: v.rule_for_each(lambda x: x.NickNames).not_null())

        person = Person(NickNames=[None, "foo", None])

        result = validator.validate(person)
        self.assertEqual(result.errors[0].PropertyName, "NickNames[0]")
        self.assertEqual(result.errors[1].PropertyName, "NickNames[2]")

    # def test_Overrides_indexer(self):
    # 	validator = TestValidator(
    # 		lambda v: v.rule_for_each(lambda x: x.NickNames).OverrideIndexer((x, collection, element, index) => {
    # 				return "<" + index + ">"
    # 		))
    # 			.not_null()
    # 	)

    # 	person = Person {
    # 		NickNames = [None,"foo",None]

    # 	result = validator.validate(person)
    # 	result.errors[0].PropertyName.ShouldEqual("NickNames<0>")
    # 	result.errors[1].PropertyName.ShouldEqual("NickNames<2>")
    # }

    # 	def public async Task Overrides_indexer_async(self):
    # 		validator = TestValidator(
    # 			lambda v: v.rule_for_each(lambda x: x.NickNames)
    # 				.OverrideIndexer((x, collection, element, index) => {
    # 					return "<" + index + ">"
    # 			))
    # 				.MustAsync((x, elem, ct) => Task.FromResult(elem is not None))
    # 	)

    # 		person = Person {
    # 			NickNames = [None,"foo",None]
    # 	)

    # 		result = await validator.ValidateAsync(person)
    # 		result.errors[0].PropertyName.ShouldEqual("NickNames<0>")
    # 		result.errors[1].PropertyName.ShouldEqual("NickNames<2>")

    # 	def public async Task Executes_rule_for_each_item_in_collection_async(self):
    # 		validator = TestValidator(
    # 			lambda v: v.rule_for_each(lambda x: x.NickNames).SetAsyncValidator(MyAsyncNotNullValidator<Person,string>())
    # 	)

    # 		person = Person {
    # 			NickNames = [None,"foo",None]
    # 	)

    # 		result = await validator.ValidateAsync(person)
    # 		result.errors.Count.ShouldEqual(2)

    # 	def public async Task Correctly_gets_collection_indices_async(self):
    # 		validator = TestValidator(
    # 			lambda v: v.rule_for_each(lambda x: x.NickNames).SetAsyncValidator(MyAsyncNotNullValidator<Person,string>())
    # 	)

    # 		person = Person {
    # 			NickNames = [None,"foo",None]
    # 	)

    # 		result = await validator.ValidateAsync(person)
    # 		result.errors[0].PropertyName.ShouldEqual("NickNames[0]")
    # 		result.errors[1].PropertyName.ShouldEqual("NickNames[2]")

    # 	def test_Nested_collection_for_null_property_should_not_throw_null_reference(self):
    # 		validator = InlineValidator<Request>()
    # 		validator.when(r => r.person is not None, () => { validator.rule_for_each(lambda x: x.person.NickNames).not_null() })

    # 		result = validator.validate(Request())
    # 		result.errors.Count.ShouldEqual(0)

    # 	def test_Should_not_scramble_property_name_when_using_collection_validators_several_levels_deep(self):
    # 		v = ApplicationViewModelValidator()
    # 		result = v.validate(ApplicationViewModel())

    # 		result.errors.Single().PropertyName.ShouldEqual("TradingExperience[0].Questions[0].SelectedAnswerID")

    # 	def public async Task Should_not_scramble_property_name_when_using_collection_validators_several_levels_deep_with_ValidateAsync(self):
    # 		v = ApplicationViewModelValidator()
    # 		result = await v.ValidateAsync(ApplicationViewModel())

    # 		result.errors.Single().PropertyName.ShouldEqual("TradingExperience[0].Questions[0].SelectedAnswerID")

    # 	def test_Uses_useful_error_message_when_used_on_non_property(self):
    # 		validator = InlineValidator[Person]()
    # 		validator.rule_for_each(lambda x: x.NickNames.AsEnumerable()).not_null()

    # 		bool thrown = False
    # 		try {
    # 			validator.validate(Person {NickNames = string[] {null, None}})
    # 	)
    # 		catch (System.InvalidOperationException ex) {
    # 			thrown = true
    # 			ex.Message.ShouldEqual("Could not infer property name for expression: lambda x: x.NickNames.AsEnumerable(). Please explicitly specify a property name by calling OverridePropertyName as part of the rule chain. Eg: RuleForEach(lambda x: x).not_null().OverridePropertyName(\"MyProperty\")")
    # 	)

    # 		thrown.ShouldBeTrue()

    # 	def public async Task RuleForEach_async_RunsTasksSynchronously(self):
    # 		validator = InlineValidator[Person]()
    # 		result = list<bool>()

    # 		validator.rule_for_each(lambda x: x.Children).MustAsync(async (person, token) =>
    # 			await ExclusiveDelay(1)
    # 				.ContinueWith(t => result.Add(t.Result), token)
    # 				.ContinueWith(t => true, token)
    # 		)

    # 		await validator.ValidateAsync(Person() {
    # 			Children = list[Person] {Person(), Person() }
    # 	))

    # 		Assert.not_empty(result)
    # 		Assert.All(result, Assert.True)

    # 	def test_Can_use_cascade_with_RuleForEach(self):
    # 		validator = InlineValidator[Person]()
    # #pragma warning disable 618
    # 		validator.rule_for_each(lambda x: x.NickNames)
    # 			.Cascade(CascadeMode.StopOnFirstFailure)
    # 			.not_null()
    # 			.not_equal("foo")
    # #pragma warning restore 618

    # 		result = validator.validate(Person {NickNames = string[] {null}})
    # 		result.errors.Count.ShouldEqual(1)

    # 	def test_Nested_conditions_Rule_For(self):
    # 		validator = InlineValidator<Request>()
    # 		validator.when(r => true, () => {
    # 			validator.when(r => r.person?.NickNames?.Any() == true, () => {
    # 				validator.rule_for(r => r.person.NickNames)
    # 					.must(nn => true)
    # 					.with_message("Failed RuleFor")
    # 		))
    # 	))
    # 		result = validator.validate(Request())
    # 		result.is_valid.ShouldBeTrue()

    # 	def test_Nested_conditions_Rule_For_Each(self):
    # 		validator = InlineValidator<Request>()

    # 		validator.when(lambda x: true, () => {
    # 			validator.when(r => r.person?.NickNames?.Any() == true, () => {
    # 				validator.rule_for_each(lambda x: x.person.NickNames)
    # 					.must(nn => true)
    # 					.with_message("Failed RuleForEach")
    # 		))
    # 	))

    # 		result = validator.validate(Request())
    # 		result.errors.Count.ShouldEqual(0)

    # 	def test_Regular_rules_can_drop_into_RuleForEach(self):
    # 		validator = TestValidator()
    # 		validator.rule_for(lambda x: x.Children)
    # 			.must(lambda x: x.Count > 2).with_message("Foo")
    # 			.ForEach(forEachElement => {
    # 				forEachElement.not_null().with_message("Bar")
    # 		))

    # 		result = validator.validate(Person {Children = list[Person] {null, None}})
    # 		result.errors.Count.ShouldEqual(3)
    # 		result.errors[0].ErrorMessage.ShouldEqual("Foo")
    # 		result.errors[0].PropertyName.ShouldEqual("Children")

    # 		result.errors[1].ErrorMessage.ShouldEqual("Bar")
    # 		result.errors[1].PropertyName.ShouldEqual("Children[0]")

    # 		result.errors[2].ErrorMessage.ShouldEqual("Bar")
    # 		result.errors[2].PropertyName.ShouldEqual("Children[1]")

    # 	def test_Resets_state_correctly_between_rules(self):
    # 		v = InlineValidator[Person]()
    # 		v.rule_for_each(lambda x: x.NickNames).not_null()
    # 		v.rule_for(lambda x: x.Forename).not_null()

    # 		# The ValidationContext is reinitialized for each item in the collection
    # 		# Specifically, the PropertyChain is reset and modified.
    # 		# After the collection has been validated, the PropertyChain should be reset to its original value.
    # 		# We can test this by checking the final output of the property names for subsequent rules after the RuleForEach.
    # 		result = v.validate(Person() {NickNames = new[] {null, "Foo", None}, Forename = None})
    # 		result.errors.Count.ShouldEqual(3)
    # 		result.errors[0].PropertyName.ShouldEqual("NickNames[0]")
    # 		result.errors[1].PropertyName.ShouldEqual("NickNames[2]")
    # 		result.errors[2].PropertyName.ShouldEqual("Forename")

    # 	def public async Task Resets_state_correctly_between_rules_async(self):
    # 		v = InlineValidator[Person]()
    # 		v.rule_for_each(lambda x: x.NickNames).not_null()
    # 		v.rule_for(lambda x: x.Forename).not_null()

    # 		# The ValidationContext is reinitialized for each item in the collection
    # 		# Specifically, the PropertyChain is reset and modified.
    # 		# After the collection has been validated, the PropertyChain should be reset to its original value.
    # 		# We can test this by checking the final output of the property names for subsequent rules after the RuleForEach.
    # 		result = await v.ValidateAsync(Person() {NickNames = new[] {null, "Foo", None}, Forename = None})
    # 		result.errors.Count.ShouldEqual(3)
    # 		result.errors[0].PropertyName.ShouldEqual("NickNames[0]")
    # 		result.errors[1].PropertyName.ShouldEqual("NickNames[2]")
    # 		result.errors[2].PropertyName.ShouldEqual("Forename")

    # 	def test_Shouldnt_throw_exception_when_configuring_rule_after_ForEach(self):
    # 		validator = InlineValidator[Person]()

    # 		validator.rule_for(lambda x: x.Orders)
    # 			.ForEach(o => {
    # 				o.must(lambda v: true)
    # 		))
    # 			.must((val) => true)
    # 			.with_message("what")

    # 		# The RuleBuilder is RuleBuilder<Person, IList[Order]>
    # 		# after the ForEach, it's returned as an IRuleBuilderOptions<Person, IEnumerable[Order]>
    # 		# This shouldn't cause an InvalidCastException when attempting to configure the rule
    # 		# by using with_message or any other standard option.

    # 		result = validator.validate(Person() {
    # 			Orders = list[Order]() { Order()}
    # 	))

    # 		result.is_valid.ShouldBeTrue()

    # 	public class ApplicationViewModel {
    # 		public list<ApplicationGroup> TradingExperience { get set } = list<ApplicationGroup> {ApplicationGroup()}

    # 	public class ApplicationGroup {
    # 		public list<Question> Questions = list<Question> {Question()}

    # 	public class Question {
    # 		public int SelectedAnswerID { get set }

    # 	public class ApplicationViewModelValidator : AbstractValidator<ApplicationViewModel> {
    # 		public ApplicationViewModelValidator() {
    # 			RuleForEach(lambda x: x.TradingExperience)
    # 				.set_validator(AppropriatenessGroupViewModelValidator())
    # 	)

    # 	public class AppropriatenessGroupViewModelValidator : AbstractValidator<ApplicationGroup> {
    # 		public AppropriatenessGroupViewModelValidator() {
    # 			RuleForEach(m => m.Questions)
    # 				.set_validator(AppropriatenessQuestionViewModelValidator())
    # 	)

    # 	public class AppropriatenessQuestionViewModelValidator : AbstractValidator<Question> {
    # 		public AppropriatenessQuestionViewModelValidator() {
    # 			RuleFor(m => m.SelectedAnswerID)
    # 				.set_validator(AppropriatenessAnswerViewModelRequiredValidator<Question, int>())

    # 	)

    # 	public class AppropriatenessAnswerViewModelRequiredValidator[T,TProperty] : PropertyValidator[T,TProperty] {

    # 		public override string Name => "AppropriatenessAnswerViewModelRequiredValidator"

    # 		public override bool IsValid(ValidationContext<T> context, TProperty value) {
    # 			return False
    # 	)

    # 	async Task<bool> ExclusiveDelay(int milliseconds) {
    # 		lock (_lock) {
    # 			if (_counter != 0) return False
    # 			_counter += 1
    # 	)

    # 		await Task.Delay(milliseconds)

    # 		lock (_lock) {
    # 			_counter -= 1
    # 	)

    # 		return true

    def test_Validates_collection(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Surname).not_null(),
            lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(OrderValidator()),
        )

        results = validator.validate(self._person)
        self.assertEqual(len(results.errors), 3)

        self.assertEqual(results.errors[1].PropertyName, "Orders[0].ProductName")
        self.assertEqual(results.errors[2].PropertyName, "Orders[1].Amount")

    def test_Collection_should_be_explicitly_included_with_expression(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Surname).not_null(),
            lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(OrderValidator()),
        )

        results = validator.validate(self._person, lambda v: (v.IncludeProperties(lambda x: x.Orders)))
        self.assertEqual(len(results.errors), 2)

    def test_Collection_should_be_explicitly_included_with_string(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Surname).not_null(),
            lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(OrderValidator()),
        )

        results = validator.validate(self._person, lambda v: v.IncludeProperties("Orders"))
        self.assertEqual(len(results.errors), 2)

    def test_Collection_should_be_excluded(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Surname).not_null(),
            lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(OrderValidator()),
        )

        results = validator.validate(self._person, lambda v: v.IncludeProperties(lambda x: x.Forename))
        self.assertEqual(len(results.errors), 0)

    def test_Condition_should_work_with_child_collection(self):
        validator = TestValidator(
            lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(OrderValidator()).when(lambda x: len(x.Orders) == 3),
        )  # there are only 2

        result = validator.validate(self._person)
        self.assertTrue(result.is_valid)

    # def public async Task Async_condition_should_work_with_child_collection(self):
    # 	validator = TestValidator(
    # 		lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(OrderValidator()).WhenAsync( (x,c) => Task.FromResult(x.Orders.Count == 3) # there are only 2
    # )

    # 	result = await validator.ValidateAsync(self._person)
    # 	result.is_valid.ShouldBeTrue()

    def test_Skips_null_items(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null(), lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(OrderValidator()))

        self._person.Orders[0] = None
        results = validator.validate(self._person)
        self.assertEqual(len(results.errors), 2)  # 2 errors - 1 for person, 1 for 2nd Order.

    def test_Can_validate_collection_using_validator_for_base_type(self):
        validator = TestValidator(
            lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(OrderInterfaceValidator()),
        )

        result = validator.validate(self._person)
        self.assertFalse(result.is_valid)

    # def test_Can_specify_condition_for_individual_collection_elements(self):
    # 	validator = TestValidator(
    # 		lambda v: v.rule_for_each(lambda x: x.Orders)
    # 			.Where(lambda x: x.ProductName is not None)
    # 			.set_validator(OrderValidator())
    # )

    # 	results = validator.validate(self._person)
    # 	self.assertEqual(len(results.errors), 1)

    # def test_Should_override_property_name(self):
    # 	validator = TestValidator(
    # 		lambda v: v.rule_for_each(lambda x: x.Orders).set_validator(OrderValidator())
    # 			.OverridePropertyName("Orders2")
    # )

    # 	results = validator.validate(self._person)
    # 	results.errors[0].PropertyName.ShouldEqual("Orders2[0].ProductName")

    def test_Top_level_collection(self):
        v = InlineValidator[list[Order]]()
        v.rule_for_each(lambda x: x).set_validator(OrderValidator())
        orders: list[Order] = [Order(), Order()]

        result = v.validate(orders)
        self.assertEqual(len(result.errors), 4)
        self.assertEqual(result.errors[0].PropertyName, "x[0].ProductName")

    # 	def test_Validates_child_validator_synchronously(self):
    # 		validator = ComplexValidationTester.TracksAsyncCallValidator[Person]()
    # 		childValidator = ComplexValidationTester.TracksAsyncCallValidator[Person]()
    # 		childValidator.rule_for(lambda x: x.Forename).not_null()
    # 		validator.rule_for_each(lambda x: x.Children).set_validator(childValidator)

    # 		validator.validate(Person() { Children = list[Person] { Person() }})
    # 		childValidator.WasCalledAsync.ShouldEqual(False)

    # 	def public async Task Validates_child_validator_asynchronously(self):
    # 		validator = ComplexValidationTester.TracksAsyncCallValidator[Person]()
    # 		childValidator = ComplexValidationTester.TracksAsyncCallValidator[Person]()
    # 		childValidator.rule_for(lambda x: x.Forename).not_null()
    # 		validator.rule_for_each(lambda x: x.Children).set_validator(childValidator)

    # 		await validator.ValidateAsync(Person() {Children = list[Person] {Person()}})
    # 		childValidator.WasCalledAsync.ShouldEqual(true)

    def test_Can_access_colletion_index(self):
        validator = InlineValidator[Person]()
        validator.rule_for_each(lambda x: x.Orders).not_null().with_message("{CollectionIndex}")
        result = validator.validate(Person(Orders=[Order(), None]))

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "1")

    # 	def public async Task Can_access_colletion_index_async(self):
    # 		validator = InlineValidator[Person]()
    # 		validator.rule_for_each(lambda x: x.Orders).MustAsync((x, ct) => Task.FromResult(x is not None)).with_message("{CollectionIndex}")
    # 		result = await validator.ValidateAsync(Person {Orders = list[Order]() {Order(), None}})
    # 		result.is_valid.ShouldBeFalse()
    # 		result.errors[0].ErrorMessage.ShouldEqual("1")

    def test_When_runs_outside_RuleForEach_loop(self):
        # Shouldn't throw an exception if the condition is run outside the loop.
        validator = InlineValidator[tuple[None | Person]]()
        validator.rule_for_each(lambda x: x[0].Orders).must(lambda x: False).when(lambda x: x[0] is not None)

        result = validator.validate((None,))
        self.assertTrue(result.is_valid)

        result = validator.validate((Person(Orders=[Order()]),))
        self.assertFalse(result.is_valid)

    # 	def public async Task When_runs_outside_RuleForEach_loop_async(self):
    # 		# Shouldn't throw an exception if the condition is run outside the loop.
    # 		validator = InlineValidator[tuple[Person]]()
    # 		validator.rule_for_each(lambda x: x[0].Orders)
    # 			.MustAsync((x,c) => Task.FromResult(False))
    # 			.when(lambda x: x[0] is not None)

    # 		result =	await validator.ValidateAsync(tuple.Create((Person) None))
    # 		result.is_valid.ShouldBeTrue()

    # 		result = await validator.ValidateAsync(tuple.Create(Person() { Orders = list[Order] { Order() }}))
    # 		result.is_valid.ShouldBeFalse()

    # def test_Can_access_parent_index(self):
    # 	personValidator = InlineValidator[Person]()
    # 	orderValidator = InlineValidator[Order]()

    # 	orderValidator.rule_for(lambda order: order.ProductName).not_empty().with_message("{CollectionIndex} must not be empty")

    # 	# Two rules - one for each collection syntax.

    # 	personValidator.rule_for(lambda x: x.Orders).not_empty().ForEach(lambda order: (order.set_validator(orderValidator)))

    # 		personValidator.rule_for_each(lambda x: x.Orders).set_validator(orderValidator)

    # 		result = personValidator.validate(Person() {
    # 			Orders = list[Order] {
    # 				Order() { ProductName =  "foo"},
    # 				Order(),
    # 				Order() { ProductName = "bar" }
    # 		)
    # 	))

    # 		result.is_valid.ShouldBeFalse()
    # 		result.errors[0].ErrorMessage.ShouldEqual("1 must not be empty")
    # 		result.errors[0].ErrorMessage.ShouldEqual("1 must not be empty")

    # 	def public async Task Can_access_parent_index_async(self):
    # 		personValidator = InlineValidator[Person]()
    # 		orderValidator = InlineValidator[Order]()

    # 		orderValidator.rule_for(lambda order: order.ProductName)
    # 			.not_empty()
    # 			.with_message("{CollectionIndex} must not be empty")

    # 		# Two rules - one for each collection syntax.

    # 		personValidator.rule_for(lambda x: x.Orders)
    # 			.not_empty()
    # 			.ForEach(lambda order: {
    # 				order.set_validator(orderValidator)
    # 		))

    # 		personValidator.rule_for_each(lambda x: x.Orders).set_validator(orderValidator)

    # 		result = await personValidator.ValidateAsync(Person() {
    # 			Orders = list[Order] {
    # 				Order() { ProductName =  "foo"},
    # 				Order(),
    # 				Order() { ProductName = "bar" }
    # 		)
    # 	))

    # 		result.is_valid.ShouldBeFalse()
    # 		result.errors[0].ErrorMessage.ShouldEqual("1 must not be empty")
    # 		result.errors[0].ErrorMessage.ShouldEqual("1 must not be empty")

    def test_Failing_condition_should_prevent_multiple_components_running_and_not_throw(self):
        # https://github.com/FluentValidation/FluentValidation/issues/1698
        validator = InlineValidator[Person]()

        validator.rule_for_each(lambda x: x.Orders).not_null().not_null().when(lambda x: len(x.Orders) > 0)

        result = validator.validate(Person())
        self.assertTrue(result.is_valid)


# 	def public async Task Failing_condition_should_prevent_multiple_components_running_and_not_throw_async(self):
# 		# https://github.com/FluentValidation/FluentValidation/issues/1698
# 		validator = InlineValidator[Person]()

# 		validator.rule_for_each(lambda x: x.Orders)
# 			.MustAsync((o, ct) => Task.FromResult(o is not None))
# 			.MustAsync((o, ct) => Task.FromResult(o is not None))
# 			.when(lambda x: x.Orders.Count > 0)

# 		result = await validator.ValidateAsync(Person())
# 		result.is_valid.ShouldBeTrue()

# 	def test_Rule_ForEach_display_name_should_match_RuleForEach_display_name(self):
# 		validator = InlineValidator[Person]()

# 		# These 2 rule definitions should produce the same error message and property name.
# 		# https://github.com/FluentValidation/FluentValidation/issues/1231

# 		validator
# 			.rule_for_each(lambda x: x.NickNames)
# 			.must(lambda x: False)
# 			.with_message("{PropertyName}")

# 		validator
# 			.rule_for(lambda x: x.NickNames)
# 			.ForEach(n => n.must(lambda x: False).with_message("{PropertyName}"))

# 		result = validator.validate(Person() {NickNames = new[] {"foo"}})
# 		result.errors[0].PropertyName.ShouldEqual("NickNames[0]")
# 		result.errors[0].ErrorMessage.ShouldEqual("Nick Names")

# 		result.errors[1].PropertyName.ShouldEqual("NickNames[0]")
# 		result.errors[1].ErrorMessage.ShouldEqual("Nick Names")


class OrderValidator(AbstractValidator[Order]):
    def __init__(self):
        super().__init__()
        self.rule_for(lambda x: x.ProductName).not_empty()
        self.rule_for(lambda x: x.Amount).not_equal(0)


class OrderInterfaceValidator(AbstractValidator[IOrder]):
    def __init__(self):
        super().__init__()
        self.rule_for(lambda x: x.Amount).not_equal(0)


if __name__ == "__main__":
    unittest.main()
