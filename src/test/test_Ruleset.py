# import unittest

# from src.fluent_validation.IValidationContext import ValidationContext
# from src.fluent_validation.InlineValidator import InlineValidator
# from src.fluent_validation.internal.PropertyChain import PropertyChain
# from src.fluent_validation.internal.RuleSetValidatorSelector import RulesetValidatorSelector
# from src.fluent_validation.results.ValidationResult import ValidationResult
# from src.test.TestValidator import TestValidator
# from src.test.person import Address, Person




# class RulesetTests(unittest.TestCase):

# 	def AssertExecuted(self, result:ValidationResult, *names:str):
# 		len_names = len(names)
# 		self.assertEqual(len(result.RuleSetsExecuted), len_names)
# 		self.assertEqual(len(result.RuleSetsExecuted & set(names)), len_names)

# 	def test_Executes_rules_in_specified_ruleset(self):
# 		validator = TestValidator()
# 		result = validator.validate(ValidationContext[Person](Person(), PropertyChain(), RulesetValidatorSelector(["Names"])))

# 		self.assertEqual(len(result.errors),2)

# 		self.AssertExecuted(result, "Names")

# 	def test_Executes_rules_not_specified_in_ruleset(self):
# 		validator = TestValidator()
# 		result = validator.validate(Person())

# 		self.assertEqual(len(result.errors),1)
# 		self.AssertExecuted(result, "default")

# 	# def test_Ruleset_cascades_to_child_validator(self):
# 	# 	addressValidator = InlineValidator[Address]()
# 	# 	addressValidator.rule_set("Test", lambda: addressValidator.rule_for(lambda x: x.Line1).not_null()
# 	# 		)

# 	# 	validator = TestValidator()

# 	# 	validator.RuleSet("Test", () => {
# 	# 		validator.RuleFor(lambda x: x.Address).SetValidator(addressValidator)
# 	# 		)

# 	# 	person = Person {
# 	# 		Address = Address()


# 	# 	result = validator.validate(ValidationContext[Person](person, PropertyChain(), RulesetValidatorSelector(new[] { "Test" })))

# 	# 	result.Errors.Count.ShouldEqual(1)
# 	# 	self.AssertExecuted(result, "Test")

# 	# def test_Ruleset_cascades_to_child_collection_validator(self):
# 	# 	orderValidator = InlineValidator<Order>()
# 	# 	orderValidator.RuleSet("Test", () => {
# 	# 		orderValidator.RuleFor(lambda x: x.ProductName).NotNull()
# 	# 		)

# 	# 	validator = TestValidator()

# 	# 	validator.RuleSet("Test", () => {
# 	# 		validator.RuleForEach(lambda x: x.Orders).SetValidator(orderValidator)
# 	# 		)

# 	# 	person = Person {
# 	# 		Orders = { Order(), Order() }


# 	# 	result = validator.validate(ValidationContext[Person](person, PropertyChain(), RulesetValidatorSelector(new[] { "Test" })))


# 	# 	result.Errors.Count.ShouldEqual(2) //one for each order
# 	# 	self.AssertExecuted(result, "Test")

# 	# def test_Executes_multiple_rulesets(self):
# 	# 	validator = TestValidator()
# 	# 	validator.RuleSet("Id", () => {
# 	# 		validator.RuleFor(lambda x: x.Id).NotEqual(0)
# 	# 		)

# 	# 	person = Person()
# 	# 	result = validator.validate(ValidationContext[Person](person, PropertyChain(), RulesetValidatorSelector(new[] { "Names", "Id" })))

# 	# 	result.Errors.Count.ShouldEqual(3)
# 	# 	self.AssertExecuted(result, "Names", "Id")

# 	# def test_Executes_all_rules(self):
# 	# 	validator = TestValidator()
# 	# 	person = Person()
# 	# 	result = validator.validate(person, v => v.IncludeAllRuleSets())
# 	# 	result.Errors.Count.ShouldEqual(3)
# 	# 	self.AssertExecuted(result, "Names", "default")

# 	# def test_Executes_rules_in_default_ruleset_and_specific_ruleset(self):
# 	# 	validator = TestValidator()
# 	# 	validator.RuleSet("foo", () => {
# 	# 		validator.RuleFor(lambda x: x.Age).NotEqual(0)
# 	# 		)

# 	# 	result = validator.validate(Person(), v => v.IncludeRulesNotInRuleSet().IncludeRuleSets("Names"))
# 	# 	result.Errors.Count.ShouldEqual(3)
# 	# 	self.AssertExecuted(result, "default", "Names")


# 	# def test_WithMessage_works_inside_rulesets(self):
# 	# 	validator = TestValidator2()
# 	# 	result = validator.validate(Person(), v => v.IncludeRuleSets("Names"))
# 	# 	Assert.Equal("foo", result.Errors[0].ErrorMessage)
# 	# 	self.AssertExecuted(result, "Names")

# 	# def test_Ruleset_selection_should_not_cascade_downwards_when_set_on_property(self):
# 	# 	validator = TestValidator4()
# 	# 	result = validator.validate(PersonContainer() { Person = Person() }, v => v.IncludeRuleSets("Names"))
# 	# 	result.IsValid.ShouldBeTrue()
# 	# 	self.AssertExecuted(result)

# 	# def test_Ruleset_selection_should_cascade_downwards_with_when_setting_child_validator_using_include_statement(self):
# 	# 	validator = TestValidator3()
# 	# 	result = validator.validate(Person(), v => v.IncludeRuleSets("Names"))
# 	# 	result.IsValid.ShouldBeFalse()
# 	# 	self.AssertExecuted(result, "Names")

# 	# def test_Ruleset_selection_should_cascade_downwards_with_when_setting_child_validator_using_include_statement_with_lambda(self):
# 	# 	validator = InlineValidator[Person]()
# 	# 	validator.Include(lambda x: TestValidator2())
# 	# 	result = validator.validate(Person(), v => v.IncludeRuleSets("Names"))
# 	# 	result.IsValid.ShouldBeFalse()


# 	# def test_Trims_spaces(self):
# 	# 	validator = InlineValidator[Person]()
# 	# 	validator.RuleSet("First", () => {
# 	# 		validator.RuleFor(lambda x: x.Forename).NotNull()
# 	# 		)
# 	# 	validator.RuleSet("Second", () => {
# 	# 		validator.RuleFor(lambda x: x.Surname).NotNull()
# 	# 		)

# 	# 	result = validator.validate(Person(), v => v.IncludeRuleSets( "First", "Second"))
# 	# 	result.Errors.Count.ShouldEqual(2)
# 	# 	self.AssertExecuted(result, "First", "Second")

# 	# def test_Applies_multiple_rulesets_to_rule(self):
# 	# 	validator = InlineValidator[Person]()
# 	# 	validator.RuleSet("First, Second", () => {
# 	# 		validator.RuleFor(lambda x: x.Forename).NotNull()
# 	# 		)

# 	# 	result = validator.validate(Person(), v => v.IncludeRuleSets("First"))
# 	# 	result.Errors.Count.ShouldEqual(1)
# 	# 	self.AssertExecuted(result, "First")

# 	# 	result = validator.validate(Person(), v => v.IncludeRuleSets("Second"))
# 	# 	result.Errors.Count.ShouldEqual(1)
# 	# 	self.AssertExecuted(result, "Second")

# 	# 	result = validator.validate(Person(), v => v.IncludeRuleSets("Third"))
# 	# 	result.Errors.Count.ShouldEqual(0)
# 	# 	self.AssertExecuted(result)

# 	# 	result = validator.validate(Person())
# 	# 	result.Errors.Count.ShouldEqual(0)
# 	# 	self.AssertExecuted(result, "default")

# 	# def test_Executes_in_rule_in_ruleset_and_default(self):
# 	# 	validator = InlineValidator[Person]()
# 	# 	validator.RuleSet("First, Default", () => {
# 	# 		validator.RuleFor(lambda x: x.Forename).NotNull()
# 	# 		)

# 	# 	result = validator.validate(Person(), v => v.IncludeRuleSets("First"))
# 	# 	result.Errors.Count.ShouldEqual(1)
# 	# 	self.AssertExecuted(result, "First")

# 	# 	result = validator.validate(Person(), v => v.IncludeRuleSets("Second"))
# 	# 	result.Errors.Count.ShouldEqual(0)
# 	# 	self.AssertExecuted(result)

# 	# 	result = validator.validate(Person())
# 	# 	result.Errors.Count.ShouldEqual(1)
# 	# 	self.AssertExecuted(result, "default")

# 	# def test_Executes_in_rule_in_default_and_none(self):
# 	# 	validator = InlineValidator[Person]()
# 	# 	validator.RuleSet("First, Default", () => {
# 	# 		validator.RuleFor(lambda x: x.Forename).NotNull()
# 	# 		)
# 	# 	validator.RuleFor(lambda x: x.Forename).NotNull()

# 	# 	result = validator.validate(Person(), v => v.IncludeRulesNotInRuleSet())
# 	# 	result.Errors.Count.ShouldEqual(2)
# 	# 	self.AssertExecuted(result, "default")

# 	# def test_Combines_rulesets_and_explicit_properties(self):
# 	# 	validator = InlineValidator[Person]()
# 	# 	validator.RuleFor(lambda x: x.Forename).NotNull()
# 	# 	validator.RuleFor(lambda x: x.Surname).NotNull()
# 	# 	validator.RuleSet("Test", () => {
# 	# 		validator.RuleFor(lambda x: x.Age).GreaterThan(0)
# 	# 		)

# 		result = validator.validate(Person(), lambda options: options.IncludeRuleSets("Test")
# 			options.IncludeProperties(lambda x: x.Forename)
# 			)

# 		result.Errors.Count.ShouldEqual(2)
# 		result.Errors[0].PropertyName.ShouldEqual("Forename")
# 		result.Errors[1].PropertyName.ShouldEqual("Age")

# 	async Task Combines_rulesets_and_explicit_properties_async() {
# 		validator = InlineValidator[Person]()
# 		validator.RuleFor(lambda x: x.Forename).MustAsync((x,t) => Task.FromResult(x != null))
# 		validator.RuleFor(lambda x: x.Surname).MustAsync((x,t) => Task.FromResult(x != null))
# 		validator.RuleSet("Test", () => {
# 			validator.RuleFor(lambda x: x.Age).MustAsync((x,t) => Task.FromResult(x > 0))
# 			)

# 		result = await validator.validateAsync(Person(), lambda options: options.IncludeRuleSets("Test")
# 			options.IncludeProperties(lambda x: x.Forename)
# 			)

# 		result.Errors.Count.ShouldEqual(2)
# 		result.Errors[0].PropertyName.ShouldEqual("Forename")
# 		result.Errors[1].PropertyName.ShouldEqual("Age")

# 	def test_Includes_combination_of_rulesets(self):
# 		validator = InlineValidator[Person]()
# 		validator.RuleFor(lambda x: x.Forename).NotNull()
# 		validator.RuleSet("Test1", () => {
# 			validator.RuleFor(lambda x: x.Surname).NotNull()
# 			)
# 		validator.RuleSet("Test2", () => {
# 			validator.RuleFor(lambda x: x.Age).GreaterThan(0)
# 			)

# 		result = validator.validate(Person(), lambda options: options.IncludeRuleSets("Test1").IncludeRulesNotInRuleSet()
# 			)

# 		result.Errors.Count.ShouldEqual(2)
# 		result.Errors[0].PropertyName.ShouldEqual("Forename")
# 		result.Errors[1].PropertyName.ShouldEqual("Surname")

# 	async Task Includes_combination_of_rulesets_async() {
# 		validator = InlineValidator[Person]()
# 		validator.RuleFor(lambda x: x.Forename).MustAsync((x,t) => Task.FromResult(x != null))
# 		validator.RuleSet("Test1", () => {
# 			validator.RuleFor(lambda x: x.Surname).MustAsync((x,t) => Task.FromResult(x != null))
# 			)
# 		validator.RuleSet("Test2", () => {
# 			validator.RuleFor(lambda x: x.Age).MustAsync((x,t) => Task.FromResult(x > 0))
# 			)

# 		result = await validator.validateAsync(Person(), lambda options: options.IncludeRuleSets("Test1").IncludeRulesNotInRuleSet()
# 			)

# 		result.Errors.Count.ShouldEqual(2)
# 		result.Errors[0].PropertyName.ShouldEqual("Forename")
# 		result.Errors[1].PropertyName.ShouldEqual("Surname")

# 	def test_Includes_all_rulesets(self):
# 		validator = InlineValidator[Person]()
# 		validator.RuleFor(lambda x: x.Forename).NotNull()
# 		validator.RuleSet("Test1", () => {
# 			validator.RuleFor(lambda x: x.Surname).NotNull()
# 			)
# 		validator.RuleSet("Test2", () => {
# 			validator.RuleFor(lambda x: x.Age).GreaterThan(0)
# 			)

# 		result = validator.validate(Person(), lambda options: options.IncludeAllRuleSets()
# 			)

# 		result.Errors.Count.ShouldEqual(3)

# 	async Task Includes_all_rulesets_async() {
# 		validator = InlineValidator[Person]()
# 		validator.RuleFor(lambda x: x.Forename).MustAsync((x,t) => Task.FromResult(x != null))
# 		validator.RuleSet("Test1", () => {
# 			validator.RuleFor(lambda x: x.Surname).MustAsync((x,t) => Task.FromResult(x != null))
# 			)
# 		validator.RuleSet("Test2", () => {
# 			validator.RuleFor(lambda x: x.Age).MustAsync((x,t) => Task.FromResult(x > 0))
# 			)

# 		result = await validator.validateAsync(Person(), lambda options: options.IncludeAllRuleSets()
# 			)

# 		result.Errors.Count.ShouldEqual(3)




# 	private class TestValidator : InlineValidator[Person] {
# 		TestValidator() {
# 			RuleSet("Names", () => {
# 				RuleFor(lambda x: x.Surname).NotNull()
# 				RuleFor(lambda x: x.Forename).NotNull()
# 				)

# 			RuleFor(lambda x: x.Id).NotEmpty()


# 	private class TestValidator2 : AbstractValidator[Person]
# 	{
# 		TestValidator2()
# 		{
# 			RuleSet("Names", () => {
# 				RuleFor(lambda x: x.Surname).NotNull().WithMessage("foo")
# 				)






# 	class TestValidator3 : AbstractValidator[Person] {
# 		TestValidator3() {
# 			Include(TestValidator2())



# 	class PersonContainer {
# 		Person Person { get set }


# 	class TestValidator4 : AbstractValidator<PersonContainer>
# 	{
# 		TestValidator4()
# 		{
# 			RuleFor(lambda x: x.Person).SetValidator(TestValidator2())

# }
