import unittest
import sys
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "fluent_validation"].pop())

from src.test.TestValidator import TestValidator
from src.test.person import Person


class SharedConditionTests(unittest.TestCase):
    # 	class SharedConditionValidator : AbstractValidator<Person> {
    # 		public SharedConditionValidator() {
    # 			# Start with a predicate to group rules together.
    # 			#
    # 			# The AbstractValidator appends this predicate
    # 			# to each inner rule_for so you only need write,
    # 			# maintain, and think about it in one place.
    # 			#
    # 			# You can finish with an Unless clause that will
    # 			# void the validation for the entire set when it's
    # 			# predicate is true.
    # 			#
    # 			when(lambda x: x.Id > 0, lambda: {
    # 				rule_for(lambda x: x.Forename).NotEmpty()
    # 				rule_for(lambda x: x.Surname).NotEmpty().Equal("Smith")
    # 			})
    # 		}
    # 	}

    # 	class SharedAsyncConditionValidator : AbstractValidator<Person> {
    # 		public SharedAsyncConditionValidator() {
    # 			# Start with a predicate to group rules together.
    # 			#
    # 			# The AbstractValidator appends this predicate
    # 			# to each inner rule_for so you only need write,
    # 			# maintain, and think about it in one place.
    # 			#
    # 			# You can finish with an Unless clause that will
    # 			# void the validation for the entire set when it's
    # 			# predicate is true.
    # 			#
    # 			WhenAsync(async (x,c) => x.Id > 0,
    # 				lambda: {
    # 					rule_for(lambda x: x.Forename).NotEmpty()
    # 					rule_for(lambda x: x.Surname).NotEmpty().Equal("Smith")
    # 				}
    # 			)
    # 		}
    # 	}

    # 	class SharedCollectionConditionValidator : AbstractValidator<Person> {
    # 		public SharedCollectionConditionValidator() {
    # 			# Start with a predicate to group rules together.
    # 			#
    # 			# The AbstractValidator appends this predicate
    # 			# to each inner rule_for so you only need write,
    # 			# maintain, and think about it in one place.
    # 			#
    # 			# You can finish with an Unless clause that will
    # 			# void the validation for the entire set when it's
    # 			# predicate is true.
    # 			#
    # 			when((x) => x.Id > 0,
    # 				lambda: {
    # 					RuleForEach(lambda x: x.NickNames).NotEmpty()
    # 				}
    # 			)
    # 		}
    # 	}

    # 	class SharedAsyncCollectionConditionValidator : AbstractValidator<Person> {
    # 		public SharedAsyncCollectionConditionValidator() {
    # 			# Start with a predicate to group rules together.
    # 			#
    # 			# The AbstractValidator appends this predicate
    # 			# to each inner rule_for so you only need write,
    # 			# maintain, and think about it in one place.
    # 			#
    # 			# You can finish with an Unless clause that will
    # 			# void the validation for the entire set when it's
    # 			# predicate is true.
    # 			#
    # 			WhenAsync(async (x,c) => x.Id > 0,
    # 				lambda: {
    # 					RuleForEach(lambda x: x.NickNames).NotEmpty()
    # 				}
    # 			)
    # 		}
    # 	}

    # 	class SharedConditionWithScopedUnlessValidator : AbstractValidator<Person> {
    # 		public SharedConditionWithScopedUnlessValidator() {
    # 			# inner rule_for() calls can contain their own,
    # 			# locally scoped when and Unless calls that
    # 			# act only on that individual rule_for() yet the
    # 			# rule_for() respects the grouped when() and
    # 			# Unless() predicates.
    # 			#
    # 			when(lambda x: x.Id > 0 && x.Age <= 65, lambda: { rule_for(lambda x: x.Orders.Count).Equal(0).Unless(lambda x: String.IsNullOrWhiteSpace(x.CreditCard) == false) })
    # 			#.Unless(lambda x: x.Age > 65)
    # 		}
    # 	}

    # 	class SharedAsyncConditionWithScopedUnlessValidator : AbstractValidator<Person> {
    # 		public SharedAsyncConditionWithScopedUnlessValidator() {
    # 			# inner rule_for() calls can contain their own,
    # 			# locally scoped when and Unless calls that
    # 			# act only on that individual rule_for() yet the
    # 			# rule_for() respects the grouped when() and
    # 			# Unless() predicates.
    # 			#
    # 			WhenAsync(async (x,c) => x.Id > 0 && x.Age <= 65,
    # 				lambda: {
    # 					rule_for(lambda x: x.Orders.Count).Equal(0).UnlessAsync(async (x,c) => String.IsNullOrWhiteSpace(x.CreditCard) == false)
    # 				}
    # 			)
    # 		}
    # 	}

    # 	class SharedConditionInverseValidator : AbstractValidator<Person> {
    # 		public SharedConditionInverseValidator() {
    # 			Unless(lambda x: x.Id == 0, lambda: { rule_for(lambda x: x.Forename).not_null() })
    # 		}
    # 	}

    # 	class SharedAsyncConditionInverseValidator : AbstractValidator<Person>
    # 	{
    # 		public SharedAsyncConditionInverseValidator()
    # 		{
    # 			UnlessAsync(async (x,c) => x.Id == 0, lambda: { rule_for(lambda x: x.Forename).not_null() })
    # 		}
    # 	}

    # 	class BadValidatorDisablesNullCheck : AbstractValidator<string> {
    # 		public BadValidatorDisablesNullCheck() {
    # 			when(lambda x: x != null, lambda: {
    # 				rule_for(lambda x: x).Must(lambda x: x != "foo")
    # 			})
    # 		}

    # 		[Obsolete("Overriding the EnsureInstanceNotNull method to prevent FluentValidation for throwing an exception for null root models is no longer supported or recommended. The ability to override this method will be removed in FluentValidation 12. For details, see https:#github.com/FluentValidation/FluentValidation/issues/2069")]
    # 		protected override void EnsureInstanceNotNull(object instanceToValidate) {
    # 			#bad.
    # 		}
    # 	}

    # 	class AsyncBadValidatorDisablesNullCheck : AbstractValidator<string> {
    # 		public AsyncBadValidatorDisablesNullCheck() {
    # 			when(lambda x: x != null, lambda: {
    # 				rule_for(lambda x: x).Must(lambda x: x != "foo")
    # 			})

    # 			WhenAsync(async (x, ct) => x != null, lambda: {
    # 				rule_for(lambda x: x).Must(lambda x: x != "foo")
    # 			})
    # 		}

    # 		[Obsolete("Overriding the EnsureInstanceNotNull method to prevent FluentValidation for throwing an exception for null root models is no longer supported or recommended. The ability to override this method will be removed in FluentValidation 12. For details, see https:#github.com/FluentValidation/FluentValidation/issues/2069")]
    # 		protected override void EnsureInstanceNotNull(object instanceToValidate) {
    # 			#bad.
    # 		}
    # 	}

    # 	def void shared_When_not_applied_to_grouped_collection_rules_when_initial_predicate_is_false() {
    # 		validator = SharedCollectionConditionValidator()
    # 		person = Person() # fails the shared when predicate

    # 		result = validator.validate(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def async Task shared_async_when_not_applied_to_grouped_collection_rules_when_initial_predicate_is_false() {
    # 		validator = SharedAsyncCollectionConditionValidator()
    # 		person = Person() # fails the shared when predicate

    # 		result = await validator.ValidateAsync(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def void Shared_When_is_applied_to_grouped_collection_rules_when_initial_predicate_is_true() {
    # 		validator = SharedCollectionConditionValidator()
    # 		person = Person() {
    # 			Id = 4, # triggers the shared when predicate
    # 			NickNames = string[] { null },
    # 		}

    # 		result = validator.validate(person)
    # 		result.Errors.Count.ShouldEqual(1)
    # 	}

    # 	def async Task Shared_async_When_is_applied_to_grouped_collection_rules_when_initial_predicate_is_true() {
    # 		validator = SharedAsyncCollectionConditionValidator()
    # 		person = Person() {
    # 			Id = 4, # triggers the shared when predicate
    # 			NickNames = string[] { null },
    # 		}

    # 		result = await validator.ValidateAsync(person)
    # 		result.Errors.Count.ShouldEqual(1)
    # 	}

    # 	def void Shared_When_is_applied_to_grouped_rules_collection_when_initial_predicate_is_true_and_all_individual_rules_are_satisfied() {
    # 		validator = SharedCollectionConditionValidator()
    # 		person = Person() {
    # 			Id = 4, # triggers the shared when predicate
    # 			NickNames = new[] { "Foo"},
    # 		}

    # 		result = validator.validate(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def async Task Shared_async_When_is_applied_to_grouped_rules_collection_when_initial_predicate_is_true_and_all_individual_rules_are_satisfied() {
    # 		validator = SharedAsyncCollectionConditionValidator()
    # 		person = Person() {
    # 			Id = 4, # triggers the shared when predicate
    # 			NickNames = new[] { "foo" }
    # 		}

    # 		result = await validator.ValidateAsync(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def void Throws_when_shared_async_condition_invoked_synchronously() {
    # 		Assert.Throws<AsyncValidatorInvokedSynchronouslyException>(lambda: {
    # 			validator = SharedAsyncCollectionConditionValidator()
    # 			person = Person() {
    # 				Id = 4, # triggers the shared when predicate
    # 				NickNames = string[] { null }
    # 			}

    # 			validator.validate(person)
    # 		})
    # 	}

    # 	def void Shared_When_is_not_applied_to_grouped_rules_when_initial_predicate_is_false() {
    # 		validator = SharedConditionValidator()
    # 		person = Person() # fails the shared when predicate

    # 		result = validator.validate(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def async Task Shared_async_When_is_not_applied_to_grouped_rules_when_initial_predicate_is_false() {
    # 		validator = SharedAsyncConditionValidator()
    # 		person = Person() # fails the shared when predicate

    # 		result = await validator.ValidateAsync(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def void Shared_When_is_applied_to_grouped_rules_when_initial_predicate_is_true() {
    # 		validator = SharedConditionValidator()
    # 		person = Person() {
    # 			Id = 4 # triggers the shared when predicate
    # 		}

    # 		result = validator.validate(person)
    # 		result.Errors.Count.ShouldEqual(3)
    # 	}

    # 	def async Task Shared_async_When_is_applied_to_grouped_rules_when_initial_predicate_is_true() {
    # 		validator = SharedAsyncConditionValidator()
    # 		person = Person() {
    # 			Id = 4 # triggers the shared when predicate
    # 		}

    # 		result = await validator.ValidateAsync(person)
    # 		result.Errors.Count.ShouldEqual(3)
    # 	}

    # 	def void Shared_When_is_applied_to_groupd_rules_when_initial_predicate_is_true_and_all_individual_rules_are_satisfied() {
    # 		validator = SharedConditionValidator()
    # 		person = Person() {
    # 			Id = 4, # triggers the shared when predicate
    # 			Forename = "Kevin", # satisfies rule_for( lambda x: x.Forename ).NotEmpty()
    # 			Surname = "Smith", # satisfies rule_for( lambda x: x.Surname ).NotEmpty().Equal( "Smith" )
    # 		}

    # 		result = validator.validate(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def async Task Shared_async_When_is_applied_to_groupd_rules_when_initial_predicate_is_true_and_all_individual_rules_are_satisfied() {
    # 		validator = SharedAsyncConditionValidator()
    # 		person = Person() {
    # 			Id = 4, # triggers the shared when predicate
    # 			Forename = "Kevin", # satisfies rule_for( lambda x: x.Forename ).NotEmpty()
    # 			Surname = "Smith", # satisfies rule_for( lambda x: x.Surname ).NotEmpty().Equal( "Smith" )
    # 		}

    # 		result = await validator.ValidateAsync(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def void Shared_When_respects_the_smaller_scope_of_an_inner_Unless_when_the_inner_Unless_predicate_is_satisfied() {
    # 		validator = SharedConditionWithScopedUnlessValidator()
    # 		person = Person() {
    # 			Id = 4 # triggers the shared when predicate
    # 		}

    # 		person.CreditCard = "1234123412341234" # satisfies the inner Unless predicate
    # 		person.Orders.Add(Order())

    # 		result = validator.validate(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def async Task Shared_async_When_respects_the_smaller_scope_of_an_inner_Unless_when_the_inner_Unless_predicate_is_satisfied() {
    # 		validator = SharedAsyncConditionWithScopedUnlessValidator()
    # 		person = Person() {
    # 			Id = 4 # triggers the shared when predicate
    # 		}

    # 		person.CreditCard = "1234123412341234" # satisfies the inner Unless predicate
    # 		person.Orders.Add(Order())

    # 		result = await validator.ValidateAsync(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def void Shared_When_respects_the_smaller_scope_of_a_inner_Unless_when_the_inner_Unless_predicate_fails() {
    # 		validator = SharedConditionWithScopedUnlessValidator()
    # 		person = Person() {
    # 			Id = 4 # triggers the shared when predicate
    # 		}

    # 		person.Orders.Add(Order()) # fails the inner Unless predicate

    # 		result = validator.validate(person)
    # 		result.Errors.Count.ShouldEqual(1)
    # 	}

    # 	def async Task Shared_async_When_respects_the_smaller_scope_of_a_inner_Unless_when_the_inner_Unless_predicate_fails() {
    # 		validator = SharedAsyncConditionWithScopedUnlessValidator()
    # 		person = Person() {
    # 			Id = 4 # triggers the shared when predicate
    # 		}

    # 		person.Orders.Add(Order()) # fails the inner Unless predicate

    # 		result = await validator.ValidateAsync(person)
    # 		result.Errors.Count.ShouldEqual(1)
    # 	}

    # 	def void Outer_Unless_clause_will_trump_an_inner_Unless_clause_when_inner_fails_but_the_outer_is_satisfied() {
    # 		validator = SharedConditionWithScopedUnlessValidator()
    # 		person = Person() {
    # 			Id = 4, # triggers the shared when predicate
    # 			Age = 70 # satisfies the outer Unless predicate
    # 		}

    # 		person.Orders.Add(Order()) # fails the inner Unless predicate

    # 		result = validator.validate(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def async Task Outer_async_Unless_clause_will_trump_an_inner_Unless_clause_when_inner_fails_but_the_outer_is_satisfied() {
    # 		validator = SharedAsyncConditionWithScopedUnlessValidator()
    # 		person = Person() {
    # 			Id = 4, # triggers the shared when predicate
    # 			Age = 70 # satisfies the outer Unless predicate
    # 		}

    # 		person.Orders.Add(Order()) # fails the inner Unless predicate

    # 		result = await validator.ValidateAsync(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def void Condition_can_be_used_inside_ruleset() {
    # 		validator = TestValidator()
    # 		validator.RuleSet("foo", lambda: { validator.when(lambda x: x.Id > 0, lambda: { validator.rule_for(lambda x: x.Forename).not_null() }) })
    # 		validator.rule_for(lambda x: x.Surname).not_null()

    # #pragma warning disable 618
    # 		result = validator.validate(Person {Id = 5}, v => v.IncludeRuleSets("foo"))
    # #pragma warning restore 618
    # 		result.Errors.Count.ShouldEqual(1)
    # 		result.Errors.Single().PropertyName.ShouldEqual("Forename")
    # 	}

    # 	def async Task Async_condition_can_be_used_inside_ruleset() {
    # 		validator = TestValidator()
    # 		validator.RuleSet("foo", lambda: {
    # 			validator.WhenAsync(async (x,c) => (x.Id > 0), lambda: {
    # 				validator.rule_for(lambda x: x.Forename).not_null()
    # 			})
    # 		})
    # 		validator.rule_for(lambda x: x.Surname).not_null()

    # 		result = await validator.ValidateAsync(Person {Id = 5}, v => v.IncludeRuleSets("foo"))
    # 		result.Errors.Count.ShouldEqual(1)
    # 		result.Errors.Single().PropertyName.ShouldEqual("Forename")
    # 	}

    # 	def void RuleSet_can_be_used_inside_condition() {
    # 		validator = TestValidator()

    # 		validator.when(lambda x: x.Id > 0, lambda: { validator.RuleSet("foo", lambda: { validator.rule_for(lambda x: x.Forename).not_null() }) })

    # 		validator.rule_for(lambda x: x.Surname).not_null()

    # 		result = validator.validate(Person {Id = 5}, v => v.IncludeRuleSets("foo"))
    # 		result.Errors.Count.ShouldEqual(1)
    # 		result.Errors.Single().PropertyName.ShouldEqual("Forename")
    # 	}

    # 	def async Task RuleSet_can_be_used_inside_async_condition() {
    # 		validator = TestValidator()

    # 		validator.WhenAsync(async (x,c) => (x.Id > 0), lambda: { validator.RuleSet("foo", lambda: { validator.rule_for(lambda x: x.Forename).not_null() }) })

    # 		validator.rule_for(lambda x: x.Surname).not_null()

    # 		result = await validator.ValidateAsync(Person {Id = 5}, v => v.IncludeRuleSets("foo"))
    # 		result.Errors.Count.ShouldEqual(1)
    # 		result.Errors.Single().PropertyName.ShouldEqual("Forename")
    # 	}

    # 	def void Rules_invoke_when_inverse_shared_condition_matches() {
    # 		validator = SharedConditionInverseValidator()
    # 		result = validator.validate(Person {Id = 1})
    # 		result.IsValid.ShouldBeFalse()
    # 	}

    # 	def async Task Rules_invoke_when_inverse_shared_async_condition_matches() {
    # 		validator = SharedAsyncConditionInverseValidator()
    # 		result = await validator.ValidateAsync(Person {Id = 1})
    # 		result.IsValid.ShouldBeFalse()
    # 	}

    # 	def void Rules_not_invoked_when_inverse_shared_condition_does_not_match() {
    # 		validator = SharedConditionInverseValidator()
    # 		result = validator.validate(Person())
    # 		result.IsValid.ShouldBeTrue()
    # 	}

    # 	def async Task Rules_not_invoked_when_inverse_shared_async_condition_does_not_match() {
    # 		validator = SharedAsyncConditionInverseValidator()
    # 		result = await validator.ValidateAsync(Person())
    # 		result.IsValid.ShouldBeTrue()
    # 	}

    # 	def async Task Does_not_execute_custom_Rule_when_condition_false() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: false, lambda: {
    # 			validator.rule_for(x=>x).Custom((x,ctx)=> ctx.AddFailure(ValidationFailure("foo", "bar")))
    # 		})

    # 		result = validator.validate(Person())
    # 		result.IsValid.ShouldBeTrue()
    # 	}

    # 	def async Task Does_not_execute_custom_Rule_when_async_condition_false() {
    # 		validator = TestValidator()
    # 		validator.WhenAsync(async (x,c) =>(false), lambda: {
    # 			validator.rule_for(x=>x).Custom((x,ctx)=> ctx.AddFailure(ValidationFailure("foo", "bar")))
    # 		})

    # 		result = await validator.ValidateAsync(Person())
    # 		result.IsValid.ShouldBeTrue()
    # 	}

    # 	def void Does_not_execute_customasync_Rule_when_condition_false()
    # 	{
    # 		validator = TestValidator()
    # 		validator.when(lambda x: false, lambda: {

    # 			validator.rule_for(x=>x).CustomAsync(async (x,ctx,c) => ctx.AddFailure(ValidationFailure("foo", "bar")))
    # 		})

    # 		result = validator.validate(Person())
    # 		result.IsValid.ShouldBeTrue()
    # 	}

    # 	def async Task Does_not_execute_customasync_Rule_when_async_condition_false() {
    # 		validator = TestValidator()
    # 		validator.WhenAsync(async (x,c) =>(false), lambda: {

    # 			validator.rule_for(x=>x).CustomAsync(async (x,ctx,c) => ctx.AddFailure(ValidationFailure("foo", "bar")))
    # 		})

    # 		result = await validator.ValidateAsync(Person())
    # 		result.IsValid.ShouldBeTrue()
    # 	}

    # 	def void Executes_custom_rule_when_condition_true() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: true, lambda: {
    # 			validator.rule_for(x=>x).Custom((x,ctx) => ctx.AddFailure(ValidationFailure("foo", "bar")))

    # 		})

    # 		result = validator.validate(Person())
    # 		result.IsValid.ShouldBeFalse()
    # 	}

    # 	def async Task Executes_custom_rule_when_async_condition_true() {
    # 		validator = TestValidator()
    # 		validator.WhenAsync(async (x,c) =>(true), lambda: {
    # 			validator.rule_for(x=>x).Custom((x,ctx) => ctx.AddFailure(ValidationFailure("foo", "bar")))

    # 		})

    # 		result = await validator.ValidateAsync(Person())
    # 		result.IsValid.ShouldBeFalse()
    # 	}

    # 	def async Task Executes_customasync_rule_when_condition_true() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: true, lambda: validator.rule_for(x=>x).CustomAsync(async (x,ctx,c) => ctx.AddFailure(ValidationFailure("foo", "bar"))))

    # 		result = await validator.ValidateAsync(Person())
    # 		result.IsValid.ShouldBeFalse()
    # 	}

    # 	def async Task Executes_customasync_rule_when_async_condition_true() {
    # 		validator = TestValidator()
    # 		validator.WhenAsync(async (x,c) =>(true), lambda: validator.rule_for(x=>x).CustomAsync(async (x,ctx,c) => ctx.AddFailure(ValidationFailure("foo", "bar"))))

    # 		result = await validator.ValidateAsync(Person())
    # 		result.IsValid.ShouldBeFalse()
    # 	}

    # 	def void Nested_conditions_with_Custom_rule() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: true, lambda: {
    # 			validator.when(lambda x: false, lambda: {
    # 				validator.rule_for(x=>x).Custom((x,ctx) => ctx.AddFailure(ValidationFailure("Custom", "The validation failed")))

    # 			})
    # 		})
    # 		result = validator.validate(Person())
    # 		result.IsValid.ShouldBeTrue()
    # 	}

    # 	def async Task Nested_async_conditions_with_Custom_rule() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: true, lambda: {
    # 			validator.WhenAsync(async (x,c) =>(false), lambda: {
    # 				validator.rule_for(x=>x).Custom((x,ctx) => ctx.AddFailure(ValidationFailure("Custom", "The validation failed")))
    # 			})
    # 		})
    # 		result = await validator.ValidateAsync(Person())
    # 		result.IsValid.ShouldBeTrue()
    # 	}

    # 	def async Task Nested_conditions_with_CustomAsync_rule() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: true, lambda: {
    # 			validator.when(lambda x: false, lambda: {
    # 				validator.rule_for(x=>x).CustomAsync(async (x,ctx,c) => ctx.AddFailure(ValidationFailure("Custom", "The validation failed")))
    # 			})
    # 		})
    # 		result = await validator.ValidateAsync(Person())
    # 		result.IsValid.ShouldBeTrue()
    # 	}

    # 	def async Task Nested_async_conditions_with_CustomAsync_rule() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: true, lambda: {
    # 			validator.WhenAsync(async (x,c) =>(false), lambda: {
    # 				validator.rule_for(x=>x).CustomAsync(async (x,ctx,c) => ctx.AddFailure(ValidationFailure("Custom", "The validation failed")))
    # 			})
    # 		})
    # 		result = await validator.ValidateAsync(Person())
    # 		result.IsValid.ShouldBeTrue()
    # 	}

    # 	def void When_condition_only_executed_once() {
    # 		validator = TestValidator()
    # 		int executions = 0
    # 		validator.when(lambda x: {
    # 			executions++
    # 			return x.Age > 10
    # 		}, lambda: {
    # 			validator.rule_for(lambda x: x.Surname).not_null()
    # 			validator.rule_for(lambda x: x.Forename).not_null()
    # 		})

    # 		validator.validate(Person(Age = 11))
    # 		executions.ShouldEqual(1)
    # 	}

    # 	def async Task WhenAsync_condition_only_executed_once() {
    # 		validator = TestValidator()
    # 		int executions = 0
    # 		validator.WhenAsync(async (x, ct) => {
    # 			executions++
    # 			return x.Age > 10
    # 		}, lambda: {
    # 			validator.rule_for(lambda x: x.Surname).not_null()
    # 			validator.rule_for(lambda x: x.Forename).not_null()
    # 		})

    # 		await validator.ValidateAsync(Person(Age = 11))
    # 		executions.ShouldEqual(1)
    # 	}

    def test_Runs_otherwise_conditions_for_When(self):
        validator = TestValidator()
        validator.when(
            lambda x: x.Age > 10,
            lambda: (validator.rule_for(lambda x: x.Forename).not_null()),
        ).Otherwise(
            lambda: validator.rule_for(lambda x: x.Surname).not_null(),
        )

        result1 = validator.validate(Person(Age=11))
        self.assertFalse(result1.is_valid)
        self.assertEqual(result1.errors[0].PropertyName, "Forename")
        result2 = validator.validate(Person(Age=9))
        self.assertFalse(result2.is_valid)
        self.assertEqual(result2.errors[0].PropertyName, "Surname")

    # def test_Runs_otherwise_conditons_for_Unless(self):
    #     validator = TestValidator()
    #     validator.Unless(
    #         lambda x: x.Age > 10,
    #         lambda: validator.rule_for(lambda x: x.Forename).not_null(),
    #     ).Otherwise(
    #         lambda: validator.rule_for(lambda x: x.Surname).not_null(),
    #     )

    #     result1 = validator.validate(Person(Age=11))
    #     self.assertEqual(result1.errors[0].PropertyName, "Surname")
    #     result2 = validator.validate(Person(Age=9))
    #     self.assertAlmostEqual(result2.errors[0].PropertyName, "Forename")


# 	def async Task Runs_otherwise_conditions_for_WhenAsync() {
# 		validator = TestValidator()
# 		validator.WhenAsync(async (x, ct) => x.Age > 10, lambda: {
# 			validator.rule_for(lambda x: x.Forename).not_null()
# 		}).Otherwise(lambda: {
# 			validator.rule_for(lambda x: x.Surname).not_null()
# 		})

# 		result1 = await validator.ValidateAsync(Person(Age = 11))
# 		result1.errors[0].PropertyName.ShouldEqual("Forename")
# 		result2 = await validator.ValidateAsync(Person(Age=9))
# 		result2.errors[0].PropertyName.ShouldEqual("Surname")
# 	}

# 	def async Task Runs_otherwise_conditions_for_UnlessAsync() {
# 		validator = TestValidator()
# 		validator.UnlessAsync(async (x, ct) => x.Age > 10, lambda: {
# 			validator.rule_for(lambda x: x.Forename).not_null()
# 		}).Otherwise(lambda: {
# 			validator.rule_for(lambda x: x.Surname).not_null()
# 		})

# 		result1 = await validator.ValidateAsync(Person(Age = 11))
# 		self.assertEqual(result1.errors[0].PropertyName,"Surname")
# 		result2 = await validator.ValidateAsync(Person(Age=9))
# 		self.assertAlmostEqual(result2.errors[0].PropertyName, "Forename")
# 	}

# 	def void Nested_when_inside_otherwise() {
# 		validator = InlineValidator<Person>()
# 		validator.when(lambda x: x.Id == 1, lambda: {
# 			validator.rule_for(lambda x: x.Forename).not_null()
# 		}).Otherwise(lambda: {
# 			validator.when(lambda x: x.Age > 18, lambda: {
# 				validator.rule_for(lambda x: x.Email).not_null()
# 			})
# 		})

# 		result = validator.validate(Person() {Id = 1})
# 		result.Errors.Count.ShouldEqual(1)
# 		result.Errors[0].PropertyName.ShouldEqual("Forename")

# 		result = validator.validate(Person() {Id = 2, Age = 20})
# 		result.Errors.Count.ShouldEqual(1)
# 		result.Errors[0].PropertyName.ShouldEqual("Email")
# 	}

# 	def void When_condition_executed_for_each_instance_of_RuleForEach_condition_should_not_be_cached() {
# 		person = Person {
# 			Children = List<Person> {
# 				Person { Id = 1},
# 				Person { Id = 0}
# 			}
# 		}

# 		childValidator = InlineValidator<Person>()
# 		int executions = 0

# 		childValidator.when(a => {
# 			executions++
# 			return a.Id != 0
# 		}, lambda: {
# 			childValidator.rule_for(a => a.Id).Equal(1)
# 		})
# 		personValidator = InlineValidator<Person>()
# 		personValidator.RuleForEach(p => p.Children).SetValidator(childValidator)

# 		validationResult = personValidator.validate(person)
# 		validationResult.IsValid.ShouldBeTrue()
# 		executions.ShouldEqual(2)
# 	}

# 	def async Task When_async_condition_executed_for_each_instance_of_RuleForEach_condition_should_not_be_cached() {
# 		person = Person {
# 			Children = List<Person> {
# 				Person { Id = 1},
# 				Person { Id = 0}
# 			}
# 		}

# 		childValidator = InlineValidator<Person>()
# 		int executions = 0

# 		childValidator.WhenAsync(async (a, ct) => {
# 			executions++
# 			return a.Id != 0
# 		}, lambda: {
# 			childValidator.rule_for(a => a.Id).Equal(1)
# 		})
# 		personValidator = InlineValidator<Person>()
# 		personValidator.RuleForEach(p => p.Children).SetValidator(childValidator)

# 		validationResult = await personValidator.ValidateAsync(person)
# 		validationResult.IsValid.ShouldBeTrue()
# 		executions.ShouldEqual(2)
# 	}

# 	def void Doesnt_throw_NullReferenceException_when_instance_not_null() {
# 		v = BadValidatorDisablesNullCheck()
# 		result = v.validate((string) null)
# 		result.IsValid.ShouldBeTrue()
# 	}

# 	def async Task Doesnt_throw_NullReferenceException_when_instance_not_null_async() {
# 		v = AsyncBadValidatorDisablesNullCheck()
# 		result = await v.ValidateAsync((string) null)
# 		result.IsValid.ShouldBeTrue()
# 	}

# 	def void Shouldnt_break_with_hashcode_collision() {
# 		v1 = InlineValidator<Collision1>()
# 		v2 = InlineValidator<Collision2>()


# 		v = InlineValidator<CollisionBase>()
# 		v.when(lambda x: x is Collision1, lambda: {
# 			v.rule_for(lambda x: ((Collision1)x).Name).not_null()
# 		})
# 		v.when(lambda x: x is Collision2, lambda: {
# 			v.rule_for(lambda x: ((Collision2)x).Name).not_null()
# 		})

# 		# shouldn't throw an InvalidCastException.
# 		containerValidator = InlineValidator<List<CollisionBase>>()
# 		containerValidator.RuleForEach(lambda x: x).SetValidator(v)
# 		containerValidator.validate(List<CollisionBase> {
# 			Collision1(), Collision2()
# 		})
# 	}

# 	def async Task Shouldnt_break_with_hashcode_collision_async() {
# 		v1 = InlineValidator<Collision1>()
# 		v2 = InlineValidator<Collision2>()

# 		v = InlineValidator<CollisionBase>()
# 		v.WhenAsync((x, ct) => Task.FromResult(x is Collision1), lambda: {
# 			v.rule_for(lambda x: ((Collision1)x).Name).not_null()
# 		})
# 		v.WhenAsync((x, ct) => Task.FromResult(x is Collision2), lambda: {
# 			v.rule_for(lambda x: ((Collision2)x).Name).not_null()
# 		})

# 		containerValidator = InlineValidator<List<CollisionBase>>()
# 		containerValidator.RuleForEach(lambda x: x).SetValidator(v)

# 		# shouldn't throw an InvalidCastException.
# 		await containerValidator.ValidateAsync(List<CollisionBase> {
# 			Collision1(), Collision2()
# 		})
# 	}


# 	class CollisionBase { }

# 	class Collision1 : CollisionBase {

# 		public string Name { get set }
# 		public override int GetHashCodelambda: 1
# 	}

# 	class Collision2 : CollisionBase {
# 		public string Name { get set }
# 		public override int GetHashCodelambda: 1
# 	}
# }

if __name__ == "__main__":
    unittest.main()
