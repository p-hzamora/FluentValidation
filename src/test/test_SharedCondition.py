# region License
# Copyright (c) .NET Foundation and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# The latest version of this file can be found at https://github.com/p-hzamora/FluentValidation
# endregion

import unittest
import sys
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

# from fluent_validation.results.ValidationFailure import ValidationFailure
from fluent_validation.InlineValidator import InlineValidator
from fluent_validation import AbstractValidator
from TestValidator import TestValidator
from person import Person


# 	class SharedConditionValidator : AbstractValidator<Person> {
# 		public SharedConditionValidator() {
# 			# Start with a predicate to group rules together.
# 			#
# 			# The AbstractValidator appends this predicate
# 			# to each inner rule_for so you only need write,
# 			# maintain, and think about it in one place.
# 			#
# 			# You can finish with an unless clause that will
# 			# void the validation for the entire set when it's
# 			# predicate is True.
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
# 			# You can finish with an unless clause that will
# 			# void the validation for the entire set when it's
# 			# predicate is True.
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
# 			# You can finish with an unless clause that will
# 			# void the validation for the entire set when it's
# 			# predicate is True.
# 			#
# 			when((x) => x.Id > 0,
# 				lambda: {
# 					rule_for_each(lambda x: x.NickNames).NotEmpty()
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
# 			# You can finish with an unless clause that will
# 			# void the validation for the entire set when it's
# 			# predicate is True.
# 			#
# 			WhenAsync(async (x,c) => x.Id > 0,
# 				lambda: {
# 					rule_for_each(lambda x: x.NickNames).NotEmpty()
# 				}
# 			)
# 		}
# 	}

# 	class SharedConditionWithScopedUnlessValidator : AbstractValidator<Person> {
# 		public SharedConditionWithScopedUnlessValidator() {
# 			# inner rule_for() calls can contain their own,
# 			# locally scoped when and unless calls that
# 			# act only on that individual rule_for() yet the
# 			# rule_for() respects the grouped when() and
# 			# unless() predicates.
# 			#
# 			when(lambda x: x.Id > 0 && x.Age <= 65, lambda: { rule_for(lambda x: x.Orders.Count).Equal(0).unless(lambda x: String.IsNullOrWhiteSpace(x.CreditCard) == False) })
# 			#.unless(lambda x: x.Age > 65)
# 		}
# 	}

# 	class SharedAsyncConditionWithScopedUnlessValidator : AbstractValidator<Person> {
# 		public SharedAsyncConditionWithScopedUnlessValidator() {
# 			# inner rule_for() calls can contain their own,
# 			# locally scoped when and unless calls that
# 			# act only on that individual rule_for() yet the
# 			# rule_for() respects the grouped when() and
# 			# unless() predicates.
# 			#
# 			WhenAsync(async (x,c) => x.Id > 0 && x.Age <= 65,
# 				lambda: {
# 					rule_for(lambda x: x.Orders.Count).Equal(0).UnlessAsync(async (x,c) => String.IsNullOrWhiteSpace(x.CreditCard) == False)
# 				}
# 			)
# 		}
# 	}

# 	class SharedConditionInverseValidator : AbstractValidator<Person> {
# 		public SharedConditionInverseValidator() {
# 			unless(lambda x: x.Id == 0, lambda: { rule_for(lambda x: x.Forename).not_null() })
# 		}
# 	}

# 	class SharedAsyncConditionInverseValidator : AbstractValidator<Person>
# 	{
# 		public SharedAsyncConditionInverseValidator()
# 		{
# 			UnlessAsync(async (x,c) => x.Id == 0, lambda: { rule_for(lambda x: x.Forename).not_null() })
# 		}
# 	}


class BadValidatorDisablesNullCheck(AbstractValidator[str]):
    def __init__(self):
        super().__init__(str)
        self.when(lambda x: x is not None, lambda: {self.rule_for(lambda x: x).must(lambda x: x != "foo")})


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
class SharedConditionTests(unittest.TestCase):
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

    # 		person.CreditCard = "1234123412341234" # satisfies the inner unless predicate
    # 		person.Orders.Add(Order())

    # 		result = validator.validate(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def async Task Shared_async_When_respects_the_smaller_scope_of_an_inner_Unless_when_the_inner_Unless_predicate_is_satisfied() {
    # 		validator = SharedAsyncConditionWithScopedUnlessValidator()
    # 		person = Person() {
    # 			Id = 4 # triggers the shared when predicate
    # 		}

    # 		person.CreditCard = "1234123412341234" # satisfies the inner unless predicate
    # 		person.Orders.Add(Order())

    # 		result = await validator.ValidateAsync(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def void Shared_When_respects_the_smaller_scope_of_a_inner_Unless_when_the_inner_Unless_predicate_fails() {
    # 		validator = SharedConditionWithScopedUnlessValidator()
    # 		person = Person() {
    # 			Id = 4 # triggers the shared when predicate
    # 		}

    # 		person.Orders.Add(Order()) # fails the inner unless predicate

    # 		result = validator.validate(person)
    # 		result.Errors.Count.ShouldEqual(1)
    # 	}

    # 	def async Task Shared_async_When_respects_the_smaller_scope_of_a_inner_Unless_when_the_inner_Unless_predicate_fails() {
    # 		validator = SharedAsyncConditionWithScopedUnlessValidator()
    # 		person = Person() {
    # 			Id = 4 # triggers the shared when predicate
    # 		}

    # 		person.Orders.Add(Order()) # fails the inner unless predicate

    # 		result = await validator.ValidateAsync(person)
    # 		result.Errors.Count.ShouldEqual(1)
    # 	}

    # 	def void Outer_Unless_clause_will_trump_an_inner_Unless_clause_when_inner_fails_but_the_outer_is_satisfied() {
    # 		validator = SharedConditionWithScopedUnlessValidator()
    # 		person = Person() {
    # 			Id = 4, # triggers the shared when predicate
    # 			Age = 70 # satisfies the outer unless predicate
    # 		}

    # 		person.Orders.Add(Order()) # fails the inner unless predicate

    # 		result = validator.validate(person)
    # 		result.Errors.Count.ShouldEqual(0)
    # 	}

    # 	def async Task Outer_async_Unless_clause_will_trump_an_inner_Unless_clause_when_inner_fails_but_the_outer_is_satisfied() {
    # 		validator = SharedAsyncConditionWithScopedUnlessValidator()
    # 		person = Person() {
    # 			Id = 4, # triggers the shared when predicate
    # 			Age = 70 # satisfies the outer unless predicate
    # 		}

    # 		person.Orders.Add(Order()) # fails the inner unless predicate

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

    def test_RuleSet_can_be_used_inside_condition(self):
        validator = TestValidator()

        validator.when(lambda x: x.Id > 0, lambda: {validator.rule_set("foo", lambda: {validator.rule_for(lambda x: x.Forename).not_null()})})

        validator.rule_for(lambda x: x.Surname).not_null()

        result = validator.validate(Person(Id=5), lambda v: v.IncludeRuleSets("foo"))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Forename")

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
    # 		result.is_valid.ShouldBeFalse()
    # 	}

    # 	def async Task Rules_invoke_when_inverse_shared_async_condition_matches() {
    # 		validator = SharedAsyncConditionInverseValidator()
    # 		result = await validator.ValidateAsync(Person {Id = 1})
    # 		result.is_valid.ShouldBeFalse()
    # 	}

    # 	def void Rules_not_invoked_when_inverse_shared_condition_does_not_match() {
    # 		validator = SharedConditionInverseValidator()
    # 		result = validator.validate(Person())
    # 		self.assertTrue(result.is_valid)
    # 	}

    # 	def async Task Rules_not_invoked_when_inverse_shared_async_condition_does_not_match() {
    # 		validator = SharedAsyncConditionInverseValidator()
    # 		result = await validator.ValidateAsync(Person())
    # 		self.assertTrue(result.is_valid)
    # 	}

    # 	def async Task Does_not_execute_custom_Rule_when_condition_false() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: False, lambda: {
    # 			validator.rule_for(lambda x: x).Custom(lambda x,ctx:ctx.AddFailure(ValidationFailure("foo", "bar")))
    # 		})

    # 		result = validator.validate(Person())
    # 		self.assertTrue(result.is_valid)
    # 	}

    # 	def async Task Does_not_execute_custom_Rule_when_async_condition_false() {
    # 		validator = TestValidator()
    # 		validator.WhenAsync(async (x,c) =>(False), lambda: {
    # 			validator.rule_for(lambda x: x).Custom(lambda x,ctx:ctx.AddFailure(ValidationFailure("foo", "bar")))
    # 		})

    # 		result = await validator.ValidateAsync(Person())
    # 		self.assertTrue(result.is_valid)
    # 	}

    # 	def void Does_not_execute_customasync_Rule_when_condition_false()
    # 	{
    # 		validator = TestValidator()
    # 		validator.when(lambda x: False, lambda: {

    # 			validator.rule_for(lambda x: x).CustomAsync(async (x,ctx,c) => ctx.AddFailure(ValidationFailure("foo", "bar")))
    # 		})

    # 		result = validator.validate(Person())
    # 		self.assertTrue(result.is_valid)
    # 	}

    # 	def async Task Does_not_execute_customasync_Rule_when_async_condition_false() {
    # 		validator = TestValidator()
    # 		validator.WhenAsync(async (x,c) =>(False), lambda: {

    # 			validator.rule_for(lambda x: x).CustomAsync(async (x,ctx,c) => ctx.AddFailure(ValidationFailure("foo", "bar")))
    # 		})

    # 		result = await validator.ValidateAsync(Person())
    # 		self.assertTrue(result.is_valid)
    # 	}

    # 	def void Executes_custom_rule_when_condition_true() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: True, lambda: {
    # 			validator.rule_for(lambda x: x).Custom(lambda x,ctx: ctx.AddFailure(ValidationFailure("foo", "bar")))

    # 		})

    # 		result = validator.validate(Person())
    # 		result.is_valid.ShouldBeFalse()
    # 	}

    # 	def async Task Executes_custom_rule_when_async_condition_true() {
    # 		validator = TestValidator()
    # 		validator.WhenAsync(async (x,c) =>(True), lambda: {
    # 			validator.rule_for(lambda x: x).Custom(lambda x,ctx: ctx.AddFailure(ValidationFailure("foo", "bar")))

    # 		})

    # 		result = await validator.ValidateAsync(Person())
    # 		result.is_valid.ShouldBeFalse()
    # 	}

    # 	def async Task Executes_customasync_rule_when_condition_true() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: True, lambda: validator.rule_for(lambda x: x).CustomAsync(async (x,ctx,c) => ctx.AddFailure(ValidationFailure("foo", "bar"))))

    # 		result = await validator.ValidateAsync(Person())
    # 		result.is_valid.ShouldBeFalse()
    # 	}

    # 	def async Task Executes_customasync_rule_when_async_condition_true() {
    # 		validator = TestValidator()
    # 		validator.WhenAsync(async (x,c) =>(True), lambda: validator.rule_for(lambda x: x).CustomAsync(async (x,ctx,c) => ctx.AddFailure(ValidationFailure("foo", "bar"))))

    # 		result = await validator.ValidateAsync(Person())
    # 		result.is_valid.ShouldBeFalse()
    # 	}

    # def test_Nested_conditions_with_Custom_rule(self):
    #     validator = TestValidator()
    #     validator.when(lambda x: True, lambda: validator.when(lambda x: False, lambda: validator.rule_for(lambda x: x).Custom(lambda x,ctx: ctx.AddFailure(ValidationFailure("Custom", "The validation failed")))))
    #     result = validator.validate(Person())
    #     self.assertTrue(result.is_valid)

    # 	def async Task Nested_async_conditions_with_Custom_rule() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: True, lambda: {
    # 			validator.WhenAsync(async (x,c) =>(False), lambda: {
    # 				validator.rule_for(lambda x: x).Custom(lambda x,ctx: ctx.AddFailure(ValidationFailure("Custom", "The validation failed")))
    # 			})
    # 		})
    # 		result = await validator.ValidateAsync(Person())
    # 		self.assertTrue(result.is_valid)
    # 	}

    # 	def async Task Nested_conditions_with_CustomAsync_rule() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: True, lambda: {
    # 			validator.when(lambda x: False, lambda: {
    # 				validator.rule_for(lambda x: x).CustomAsync(async (x,ctx,c) => ctx.AddFailure(ValidationFailure("Custom", "The validation failed")))
    # 			})
    # 		})
    # 		result = await validator.ValidateAsync(Person())
    # 		self.assertTrue(result.is_valid)
    # 	}

    # 	def async Task Nested_async_conditions_with_CustomAsync_rule() {
    # 		validator = TestValidator()
    # 		validator.when(lambda x: True, lambda: {
    # 			validator.WhenAsync(async (x,c) =>(False), lambda: {
    # 				validator.rule_for(lambda x: x).CustomAsync(async (x,ctx,c) => ctx.AddFailure(ValidationFailure("Custom", "The validation failed")))
    # 			})
    # 		})
    # 		result = await validator.ValidateAsync(Person())
    # 		self.assertTrue(result.is_valid)
    # 	}

    def test_When_condition_only_executed_once(self):
        validator = TestValidator()

        executions: int = 0

        def lambda_(a: Person):
            nonlocal executions
            executions += 1
            return a.Age > 0

        validator.when(lambda_, lambda: (validator.rule_for(lambda x: x.Surname).not_null(), validator.rule_for(lambda x: x.Forename).not_null()))

        validator.validate(Person(Age=11))
        self.assertEqual(executions, 1)

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
            lambda: validator.rule_for(lambda x: x.Forename).not_null(),
        ).otherwise(
            lambda: validator.rule_for(lambda x: x.Surname).not_null(),
        )

        result1 = validator.validate(Person(Age=11))
        self.assertFalse(result1.is_valid)
        self.assertEqual(result1.errors[0].PropertyName, "Forename")
        result2 = validator.validate(Person(Age=9))
        self.assertFalse(result2.is_valid)
        self.assertEqual(result2.errors[0].PropertyName, "Surname")

    def test_Runs_otherwise_conditons_for_Unless(self):
        validator = TestValidator()
        validator.unless(
            lambda x: x.Age > 10,
            lambda: validator.rule_for(lambda x: x.Forename).not_null(),
        ).otherwise(
            lambda: validator.rule_for(lambda x: x.Surname).not_null(),
        )

        result1 = validator.validate(Person(Age=11))
        self.assertEqual(result1.errors[0].PropertyName, "Surname")
        result2 = validator.validate(Person(Age=9))
        self.assertAlmostEqual(result2.errors[0].PropertyName, "Forename")

    # 	def async Task Runs_otherwise_conditions_for_WhenAsync() {
    # 		validator = TestValidator()
    # 		validator.WhenAsync(async (x, ct) => x.Age > 10, lambda: {
    # 			validator.rule_for(lambda x: x.Forename).not_null()
    # 		}).otherwise(lambda: {
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
    # 		}).otherwise(lambda: {
    # 			validator.rule_for(lambda x: x.Surname).not_null()
    # 		})

    # 		result1 = await validator.ValidateAsync(Person(Age = 11))
    # 		self.assertEqual(result1.errors[0].PropertyName,"Surname")
    # 		result2 = await validator.ValidateAsync(Person(Age=9))
    # 		self.assertAlmostEqual(result2.errors[0].PropertyName, "Forename")
    # 	}

    def test_Nested_when_inside_otherwise(self):
        validator = InlineValidator[Person](Person)
        (
            validator.when(
                lambda x: x.Id == 1,
                lambda: validator.rule_for(lambda x: x.Forename).not_null(),
            ).otherwise(
                lambda: validator.when(
                    lambda x: x.Age > 18,
                    lambda: validator.rule_for(lambda x: x.Email).not_null(),
                )
            )
        )

        result = validator.validate(Person(Id=1))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Forename")

        result = validator.validate(Person(Id=2, Age=20))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Email")

    def test_When_condition_executed_for_each_instance_of_RuleForEach_condition_should_not_be_cached(self):
        person = Person(
            Children=[
                Person(Id=1),
                Person(Id=0),
            ]
        )

        childValidator = InlineValidator[Person](Person)
        executions: int = 0

        def lambda_(a: Person):
            nonlocal executions
            executions += 1
            return a.Id != 0

        childValidator.when(lambda_, lambda: (childValidator.rule_for(lambda a: a.Id).equal(1)))
        personValidator = InlineValidator[Person](Person)
        personValidator.rule_for_each(lambda p: p.Children).set_validator(childValidator)

        validationResult = personValidator.validate(person)
        self.assertTrue(validationResult.is_valid)
        self.assertEqual(executions, 2)

    # 	def async Task When_async_condition_executed_for_each_instance_of_RuleForEach_condition_should_not_be_cached() {
    # 		person = Person {
    # 			Children = list<Person> {
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
    # 		personValidator.rule_for_each(p => p.Children).SetValidator(childValidator)

    # 		validationResult = await personValidator.ValidateAsync(person)
    # 		validationResult.is_valid.ShouldBeTrue()
    # 		executions.ShouldEqual(2)
    # 	}

    def test_Doesnt_throw_NullReferenceException_when_instance_not_null(self) -> None:
        v = BadValidatorDisablesNullCheck()
        result = v.validate(str, None)
        self.assertTrue(result.is_valid)

    # 	def async Task Doesnt_throw_NullReferenceException_when_instance_not_null_async() {
    # 		v = AsyncBadValidatorDisablesNullCheck()
    # 		result = await v.ValidateAsync((string) null)
    # 		self.assertTrue(result.is_valid)
    # 	}

    # def test_Shouldnt_break_with_hashcode_collision(self):
    #     v1 = InlineValidator(Collision1)
    #     v2 = InlineValidator(Collision2)

    #     v = InlineValidator(CollisionBase)
    #     v.when(lambda x: x, lambda: (v.rule_for(lambda x: x.Name).not_null()))

    #     v.when(lambda x: x, lambda: v.rule_for(lambda x: x.Name).not_null())

    #     # shouldn't throw an InvalidCastException.
    #     containerValidator = InlineValidator(list[CollisionBase])
    #     containerValidator.rule_for_each(lambda x: x).set_validator(v)
    #     containerValidator.validate([Collision1(), Collision2()])


# 	def async Task Shouldnt_break_with_hashcode_collision_async() {
# 		v1 = InlineValidator[Collision1](Collision1)
# 		v2 = InlineValidator[Collision2](Collision2)

# 		v = InlineValidator[CollisionBase](CollisionBase)
# 		v.WhenAsync((x, ct) => Task.FromResult(x is Collision1), lambda: {
# 			v.rule_for(lambda x: ((Collision1)x).Name).not_null()
# 		})
# 		v.WhenAsync((x, ct) => Task.FromResult(x is Collision2), lambda: {
# 			v.rule_for(lambda x: ((Collision2)x).Name).not_null()
# 		})

# 		containerValidator = InlineValidator<list[CollisionBase]>()
# 		containerValidator.rule_for_each(lambda x: x).SetValidator(v)

# 		# shouldn't throw an InvalidCastException.
# 		await containerValidator.ValidateAsync(list[CollisionBase] {
# 			Collision1(), Collision2()
# 		})
# 	}


class CollisionBase: ...


class Collision1(CollisionBase):
    def __init__(self):
        self.Name = None

    def __hash__(self):
        return 1


class Collision2(CollisionBase):
    def __init__(self):
        self.Name = None

    def __hash__(self):
        return 1


if __name__ == "__main__":
    unittest.main()
