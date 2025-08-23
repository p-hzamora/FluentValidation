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

from TestValidator import TestValidator
from person import Person
from fluent_validation.InlineValidator import InlineValidator
# from fluent_validation.abstract_validator import AbstractValidator


# class AsyncValidator(AbstractValidator[int]):
#     def __init__(self):
#         super().__init__(int)
#         self.rule_for(lambda model: model).must_async(lambda ie, ct: asyncio.create_task(self._async_validation_1(ie))).dependent_rules(
#             lambda: self.rule_for(lambda m: m).must_async(lambda ie, ct: asyncio.create_task(self._async_validation_2(ie)))
#         )

#     async def _async_validation_1(self, value):
#         await asyncio.sleep(0.5)
#         return True

#     async def _async_validation_2(self, value):
#         await asyncio.sleep(1.0)
#         return False


# class AsyncValidator2(AbstractValidator[int]):
#     def __init__(self):
#         super().__init__(int)
#         self.rule_for(lambda model: model).must(lambda ie: True).dependent_rules(lambda: self.rule_for(lambda m: m).must_async(lambda ie, ct: asyncio.create_task(self._async_validation(ie))))

#     async def _async_validation(self, value):
#         await asyncio.sleep(1.0)
#         return False


class RuleDependencyTests(unittest.TestCase):
    def test_Invokes_dependent_rule_if_parent_rule_passes(self):
        validator = TestValidator()
        validator.rule_for(lambda x: x.Surname).not_null().dependent_rules(lambda: validator.rule_for(lambda x: x.Forename).not_null())

        results = validator.validate(Person(Surname="foo"))
        self.assertEqual(len(results.errors), 1)
        self.assertEqual(results.errors[0].PropertyName, "Forename")

    def test_Does_not_invoke_dependent_rule_if_parent_rule_does_not_pass(self):
        validator = TestValidator()
        validator.rule_for(lambda x: x.Surname).not_null().dependent_rules(lambda: validator.rule_for(lambda x: x.Forename).not_null())

        results = validator.validate(Person(Surname=None))
        self.assertEqual(len(results.errors), 1)
        self.assertEqual(results.errors[0].PropertyName, "Surname")

    def test_Nested_dependent_rules(self):
        validator = TestValidator()
        validator.rule_for(lambda x: x.Surname).not_null().dependent_rules(
            lambda: validator.rule_for(lambda x: x.Forename).not_null().dependent_rules(lambda: validator.rule_for(lambda x: x.Forename).not_equal("foo"))
        )

        results = validator.validate(Person(Surname="foo"))
        self.assertEqual(len(results.errors), 1)
        self.assertEqual(results.errors[0].PropertyName, "Forename")
        # Note: Additional checks for dependent rule structure would need implementation

    def test_Dependent_rules_inside_ruleset(self):
        validator = TestValidator()
        # fmt: off
        validator.rule_set("MyRuleSet", lambda: 
                           
            validator.rule_for(lambda x: x.Surname).not_null()
                .dependent_rules(lambda: 
                    validator.rule_for(lambda x: x.Forename).not_null()))

        # fmt: on
        results = validator.validate(Person(Surname="foo"), lambda x: x.IncludeRuleSets("MyRuleSet"))
        self.assertEqual(len(results.errors), 1)
        self.assertEqual(results.errors[0].PropertyName, "Forename")

    def test_Dependent_rules_inside_when(self):
        validator = TestValidator()
        # fmt: off
        validator.when(lambda o: o.Forename is not None, lambda: 
                       validator.rule_for(lambda o: o.Age).less_than(1)
                       
                       .dependent_rules(lambda: 
                                       
                            validator.rule_for(lambda o: o.Forename).not_null()))
        # fmt: on
        result = validator.validate(Person())
        self.assertTrue(result.is_valid)

    # async def test_TestAsyncWithdependent_rules_SyncEntry(self):
    #     validator = TestValidator()
    #     validator.rule_for(lambda o: o.Forename).not_null().dependent_rules(
    #         lambda: [validator.rule_for(lambda o: o.Address).not_null(), validator.rule_for(lambda o: o.Age).must_async(lambda p, token: asyncio.create_task(self._async_age_check(p)))]
    #     )

    #     result = await validator.validateAsync(Person())
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertTrue(any(x.PropertyName == "Forename" for x in result.errors))

    #     result = await validator.validateAsync(Person(Forename="Foo"))
    #     self.assertEqual(len(result.errors), 2)
    #     self.assertEqual(len([x for x in result.errors if x.PropertyName == "Address"]), 1)
    #     self.assertEqual(len([x for x in result.errors if x.PropertyName == "Age"]), 1)

    # async def test_TestAsyncWithdependent_rules_AsyncEntry(self):
    #     validator = TestValidator()
    #     validator.rule_for(lambda o: o).must_async(lambda p, ct: asyncio.create_task(self._async_person_check(p))).dependent_rules(
    #         lambda: [validator.rule_for(lambda o: o.Address).not_null(), validator.rule_for(lambda o: o.Age).must_async(lambda p, token: asyncio.create_task(self._async_age_check(p)))]
    #     )

    #     result = await validator.validateAsync(Person())
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertTrue(any(x.PropertyName == "" for x in result.errors))

    #     result = await validator.validateAsync(Person(Forename="Foo"))
    #     self.assertEqual(len(result.errors), 2)
    #     self.assertEqual(len([x for x in result.errors if x.PropertyName == "Address"]), 1)
    #     self.assertEqual(len([x for x in result.errors if x.PropertyName == "Age"]), 1)

    # async def test_Async_inside_dependent_rules(self):
    #     validator = AsyncValidator()
    #     result = await validator.validateAsync(0)
    #     self.assertFalse(result.is_valid)

    # async def test_Async_inside_dependent_rules_when_parent_rule_not_async(self):
    #     validator = AsyncValidator2()
    #     result = await validator.validateAsync(0)
    #     self.assertFalse(result.is_valid)

    def test_Treats_root_level_rule_for_call_as_dependent_rule_if_user_forgets_to_use_dependent_rulesBuilder(self):
        validator = TestValidator()
        # fmt: off
        (

        validator.rule_for(lambda x: x.Surname).not_null()
         
        .dependent_rules(lambda: 
                validator.rule_for(lambda x: x.Forename).not_null()  # Shouldn't be invoked
        )
        )
        # fmt: on

        results = validator.validate(Person(Surname=None))
        self.assertEqual(len(results.errors), 1)  # only the root not_null should fire
        self.assertEqual(results.errors[0].PropertyName, "Surname")

    def test_Nested_dependent_rules_inside_ruleset(self):
        validator = TestValidator()

        # fmt: off
        validator.rule_set("MyRuleSet",lambda: 
                           
            validator.rule_for(lambda x: x.Surname).not_null()
            .dependent_rules(lambda:  
                                   
                    validator.rule_for(lambda x: x.Forename).not_null()
                    .dependent_rules(lambda:  
                                            
                        validator.rule_for(lambda x: x.Address).not_null())),
        )
        # fmt: on

        results = validator.validate(Person(Surname="foo", Forename="foo"), lambda v: v.IncludeRuleSets("MyRuleSet"))
        self.assertEqual(len(results.errors), 1)
        self.assertEqual(results.errors[0].PropertyName, "Address")

    def test_Nested_dependent_rules_inside_ruleset_no_result_when_top_level_fails(self):
        validator = TestValidator()

        # fmt: off
        validator.rule_set("MyRuleSet",lambda: 
            validator.rule_for(lambda x: x.Surname).not_null()
            
            .dependent_rules(lambda: 
                    validator.rule_for(lambda x: x.Forename).not_null()
                    
                    .dependent_rules(lambda: 
                            validator.rule_for(lambda x: x.Address).not_null())),
        )
        # fmt:on

        results = validator.validate(Person(Surname=None, Forename="foo"), lambda v: v.IncludeRuleSets("MyRuleSet"))
        self.assertEqual(len(results.errors), 1)
        self.assertEqual(results.errors[0].PropertyName, "Surname")

    def test_Nested_dependent_rules_inside_ruleset_no_result_when_second_level_fails(self):
        validator = TestValidator()

        # fmt: off
        validator.rule_set(
            "MyRuleSet",

            lambda: validator.rule_for(lambda x: x.Surname).not_null()

            .dependent_rules(lambda: 
                
                validator.rule_for(lambda x: x.Forename).not_null()
                
                .dependent_rules(lambda: 
                                
                    validator.rule_for(lambda x: x.Address).not_null())),
        )
        # fmt: on

        results = validator.validate(Person(Surname="bar", Forename=None), lambda v: v.IncludeRuleSets("MyRuleSet"))
        self.assertEqual(len(results.errors), 1)
        self.assertEqual(results.errors[0].PropertyName, "Forename")

    def test_Nested_dependent_rules_inside_ruleset_inside_method(self):
        validator = TestValidator()
        # fmt: off
        validator.rule_set("MyRuleSet",lambda: 
                           
            validator.rule_for(lambda x: x.Surname).not_null()

            .dependent_rules(lambda: 
                
                    validator.rule_for(lambda x: x.Forename).not_null()
                    
                    .dependent_rules(lambda: 
                            
                            self.BaseValidation(validator))),
        )
        # fmt: on

        results = validator.validate(Person(Surname="foo", Forename="foo"), lambda v: v.IncludeRuleSets("MyRuleSet"))
        self.assertEqual(len(results.errors), 1)
        self.assertEqual(results.errors[0].PropertyName, "Address")

    # FIXME [x]: Custom method it's not included at this moment
    def test_Invokes_dependent_rule_if_parent_custom_rule_passes(self):
        validator = TestValidator()
        validator.rule_for(lambda x: x.Surname).custom(lambda name, context: None).dependent_rules(lambda: validator.rule_for(lambda x: x.Forename).not_null())

        results = validator.validate(Person(Surname="foo"))
        self.assertEqual(len(results.errors), 1)
        self.assertEqual(results.errors[0].PropertyName, "Forename")

    def test_Does_not_invoke_dependent_rule_if_parent_custom_rule_does_not_pass(self):
        validator = TestValidator()
        # fmt:off
        validator.rule_for(lambda x: x.Surname).custom(lambda name, context: (
            context.AddFailure(errorMessage="Failed")
            )
        ).dependent_rules(lambda: 
            validator.rule_for(lambda x: x.Forename).not_null())
        # fmt:on

        results = validator.validate(Person(Surname=None))
        self.assertEqual(len(results.errors), 1)
        self.assertEqual(results.errors[0].PropertyName, "Surname")

    def BaseValidation(self, validator: InlineValidator[Person]):
        validator.rule_for(lambda x: x.Address).not_null()

    # async def _async_age_check(self, age):
    #     return age > 10

    # async def _async_person_check(self, person):
    #     return person.Forename is not None


if __name__ == "__main__":
    unittest.main()
