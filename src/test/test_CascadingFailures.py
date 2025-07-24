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


from fluent_validation.ValidatorOptions import ValidatorOptions
from fluent_validation.internal.TrackingCollection import IDisposable
from TestValidator import TestValidator
from person import Person  # , Order
from fluent_validation import CascadeMode


class CascadingFailuresTester(unittest.TestCase, IDisposable):
    def setUp(self):
        self.SetBothGlobalCascadeModes(CascadeMode.Continue)
        self._validator: TestValidator = TestValidator()

    def tearDown(self):
        ValidatorOptions.Global.DefaultClassLevelCascadeMode = CascadeMode.Continue
        ValidatorOptions.Global.DefaultRuleLevelCascadeMode = CascadeMode.Continue

    def Dispose(self) -> None:
        self.SetBothGlobalCascadeModes(CascadeMode.Continue)

    def __enter__(self): ...
    def __exit__(self):
        return self.Dispose()

    def test_Validation_continues_on_failure(self):
        self._validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_stops_on_first_rule_level_failure(self):
        self.SetBothGlobalCascadeModes(CascadeMode.Stop)

        self._validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Validation_stops_on_first_rule_level_failure_and_evaluates_other_rules_when_globaldefault_rule_Stop(self):
        ValidatorOptions.Global.DefaultRuleLevelCascadeMode = CascadeMode.Stop

        self._validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        self._validator.rule_for(lambda x: x.Forename).not_null().equal("Foo")
        self._validator.rule_for(lambda x: x.Email).not_null().equal("Foo")

        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 3)

    def test_Validation_stops_after_first_rule_failure_when_globaldefault_class_Stop(self):
        ValidatorOptions.Global.DefaultClassLevelCascadeMode = CascadeMode.Stop

        self._validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        self._validator.rule_for(lambda x: x.Forename).not_null().equal("Foo")
        self._validator.rule_for(lambda x: x.Email).not_null().equal("Foo")

        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_continues_on_failure_when_globaldefault_both_Stop_and_ruleleveloverride_Continue(self):
        self.SetBothGlobalCascadeModes(CascadeMode.Stop)

        self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).not_null().equal("Foo")
        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_continues_on_failure_when_globaldefault_rule_stop_and_ruleleveloverride_Continue(self):
        ValidatorOptions.Global.DefaultRuleLevelCascadeMode = CascadeMode.Stop

        self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).not_null().equal("Foo")
        self._validator.rule_for(lambda x: x.Forename).Cascade(CascadeMode.Continue).not_null().equal("Foo")
        self._validator.rule_for(lambda x: x.Email).Cascade(CascadeMode.Continue).not_null().equal("Foo")

        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 6)

    def test_Validation_stops_after_first_rule_failure_when_globaldefault_class_stop_and_ruleleveloverride_Continue(self):
        ValidatorOptions.Global.DefaultClassLevelCascadeMode = CascadeMode.Stop

        self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).not_null().equal("Foo")
        self._validator.rule_for(lambda x: x.Forename).Cascade(CascadeMode.Continue).not_null().equal("Foo")
        self._validator.rule_for(lambda x: x.Email).Cascade(CascadeMode.Continue).not_null().equal("Foo")

        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_stops_on_first_failure_when_globaldefault_both_Continue_and_ruleleveloverride_Stop(self):
        self.SetBothGlobalCascadeModes(CascadeMode.Continue)
        self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).not_null().equal("Foo")
        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    # def test_Validation_stops_on_first_failure_when_globaldefault_both_Continue_and_ruleleveloverride_Stop_legacy(self):
    # 	self.SetBothGlobalCascadeModes(CascadeMode.Continue)
    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.StopOnFirstFailure).not_null().equal("Foo")
    # 	results = self._validator.validate(Person())
    # 	self.assertEqual(len(results.errors), 1)

    def test_Validation_continues_to_second_validator_when_first_validator_succeeds_and_globaldefault_both_Stop(self):
        self.SetBothGlobalCascadeModes(CascadeMode.Stop)
        self._validator.rule_for(lambda x: x.Surname).not_null().length(2, 10)
        result = self._validator.validate(Person(Surname="x"))
        self.assertFalse(result.is_valid)

    def test_Validation_continues_to_first_failing_validator_then_stops_in_all_rules_when_first_validator_succeeds_and_globaldefault_rule_Stop(self):
        ValidatorOptions.Global.DefaultRuleLevelCascadeMode = CascadeMode.Stop

        self._validator.rule_for(lambda x: x.Surname).not_null().equal("Foo").length(2, 10)
        self._validator.rule_for(lambda x: x.Forename).not_null().equal("Foo").length(2, 10)
        self._validator.rule_for(lambda x: x.Email).not_null().equal("Foo").length(2, 10)
        self._validator.rule_for(lambda x: x.CreditCard).not_null().equal("Foo").length(2, 10)

        result = self._validator.validate(Person(Surname="x", Forename="x", Email="x", CreditCard="x"))

        self.assertEqual(len(result.errors), 4)

    def test_Validation_stops_after_first_rule_when_first_rule_fails_and_globaldefault_class_Stop(self):
        ValidatorOptions.Global.DefaultClassLevelCascadeMode = CascadeMode.Stop

        self._validator.rule_for(lambda x: x.Surname).not_null().equal("Foo").length(2, 10)
        self._validator.rule_for(lambda x: x.Forename).not_null().equal("Foo").length(2, 10)
        self._validator.rule_for(lambda x: x.Email).not_null().equal("Foo").length(2, 10)
        self._validator.rule_for(lambda x: x.CreditCard).not_null().equal("Foo").length(2, 10)

        result = self._validator.validate(Person(Surname="x", Forename="x", Email="x", CreditCard="x"))

        self.assertEqual(len(result.errors), 2)

    def test_Validation_stops_on_first_failure_when_classlevel_Stop_and_ruleleveldefault_Stop(self):
        self.SetBothValidatorCascadeModes(CascadeMode.Stop)

        self._validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        self._validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Validation_stops_on_first_failure_when_ruleleveldefault_Stop(self):
        self._validator.RuleLevelCascadeMode = CascadeMode.Stop

        self._validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Validation_continues_when_classlevel_Continue_and_ruleleveldefault_Continue(self):
        self.SetBothValidatorCascadeModes(CascadeMode.Continue)

        self._validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_continues_on_failure_when_classlevel_Stop_and_ruleleveldefault_Stop_and_ruleleveloverride_Continue(self):
        self.SetBothValidatorCascadeModes(CascadeMode.Stop)

        self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).not_null().equal("Foo")
        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_continues_on_failure_when_ruleleveldefault_Stop_and_ruleleveloverride_Continue(self):
        self._validator.RuleLevelCascadeMode = CascadeMode.Stop

        self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).not_null().equal("Foo")
        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_stops_on_failure_when_classlevel_Continue_and_ruleleveldefault_Continue_and_ruleleveloverride_Stop(self):
        self.SetBothValidatorCascadeModes(CascadeMode.Continue)

        self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).not_null().equal("Foo")
        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    # def test_Validation_stops_on_failure_when_classlevel_Continue_and_ruleleveldefault_Continue_and_ruleleveloverride_Stop_legacy(self):
    # 	self.SetBothValidatorCascadeModes(CascadeMode.Continue)

    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.StopOnFirstFailure).not_null().equal("Foo")
    # 	results = self._validator.validate(Person())
    # 	self.assertEqual(len(results.errors), 1)

    def test_Cascade_mode_can_be_set_after_validator_instantiated(self):
        self._validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        self.SetBothValidatorCascadeModes(CascadeMode.Stop)
        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Cascade_mode_can_be_set_after_validator_instantiated_legacy(self):
        self._validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        self._validator.RuleLevelCascadeMode = CascadeMode.Stop
        results = self._validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    # async def test_Validation_continues_on_failure_async(self):
    # 	self._validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 2)

    # async def test_Validation_stops_on_first_failure_async(self):
    # 	self.SetBothGlobalCascadeModes(CascadeMode.Stop)

    # 	self._validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_stops_on_first_rule_level_failure_when_globaldefault_rule_Stop_async(self):
    # 	ValidatorOptions.Global.DefaultRuleLevelCascadeMode = CascadeMode.Stop

    # 	self._validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self._validator.rule_for(lambda x: x.Forename).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self._validator.rule_for(lambda x: x.Email).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")

    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 3)

    # async def test_Validation_stops_after_first_rule_failure_when_globaldefault_class_Stop_async(self):
    # 	ValidatorOptions.Global.DefaultClassLevelCascadeMode = CascadeMode.Stop

    # 	self._validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self._validator.rule_for(lambda x: x.Forename).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self._validator.rule_for(lambda x: x.Email).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 2)

    # async def test_Validation_continues_on_failure_when_globaldefault_both_Stop_and_ruleleveloverride_Continue_async(self):
    # 	self.SetBothGlobalCascadeModes(CascadeMode.Stop)

    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 2)

    # async def test_Validation_continues_on_failure_when_globaldefault_rule_stop_and_ruleleveloverride_Continue_async(self):
    # 	ValidatorOptions.Global.DefaultRuleLevelCascadeMode = CascadeMode.Stop

    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self._validator.rule_for(lambda x: x.Forename).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self._validator.rule_for(lambda x: x.Email).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")

    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 6)

    # async def test_Validation_stops_after_first_rule_failure_when_globaldefault_class_stop_and_ruleleveloverride_Continue_async(self):
    # 	ValidatorOptions.Global.DefaultClassLevelCascadeMode = CascadeMode.Stop

    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self._validator.rule_for(lambda x: x.Forename).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self._validator.rule_for(lambda x: x.Email).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")

    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 2)

    # async def test_Validation_stops_on_first_Failure_when_globaldefault_both_Continue_and_ruleleveloverride_Stop_async(self):
    # 	self.SetBothGlobalCascadeModes(CascadeMode.Continue)
    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_stops_on_first_Failure_when_globaldefault_both_Continue_and_ruleleveloverride_Stop_async_legacy(self):
    # 	self.SetBothGlobalCascadeModes(CascadeMode.Continue)
    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.StopOnFirstFailure).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_stops_on_first_Failure_when_globaldefault_both_Continue_and_ruleleveloverride_Stop_async_and_async_validator_is_invoked_synchronously(self):
    # 	self.SetBothGlobalCascadeModes(CascadeMode.Continue)
    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).not_null().equal("Foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_stops_on_first_Failure_when_globaldefault_both_Continue_and_ruleleveloverride_Stop_async_and_async_validator_is_invoked_synchronously_legacy(self):
    # 	self.SetBothGlobalCascadeModes(CascadeMode.Continue)
    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.StopOnFirstFailure).not_null().equal("Foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_continues_to_second_validator_when_first_validator_succeeds_and_globaldefault_both_Stop_async(self):
    # 	self.SetBothGlobalCascadeModes(CascadeMode.Stop)
    # 	self._validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	result = await self._validator.ValidateAsync(Person( Surname = "x" ))
    # 	result.IsValid.ShouldBeFalse()

    # async def test_Validation_continues_to_first_failing_validator_then_stops_in_all_rules_when_first_validator_succeeds_and_globaldefault_rule_Stop_async(self):
    # 	ValidatorOptions.Global.DefaultRuleLevelCascadeMode = CascadeMode.Stop

    # 	self._validator.rule_for(lambda x: x.Surname)
    # 		.MustAsync(async (x, c) => x != null)
    # 		.MustAsync(async (x, c) => x.length >= 2)
    # 		.MustAsync(async (x, c) => x == "foo")

    # 	self._validator.rule_for(lambda x: x.Forename)
    # 		.MustAsync(async (x, c) => x != null)
    # 		.MustAsync(async (x, c) => x.length >= 2)
    # 		.MustAsync(async (x, c) => x == "foo")

    # 	self._validator.rule_for(lambda x: x.Email)
    # 		.MustAsync(async (x, c) => x != null)
    # 		.MustAsync(async (x, c) => x.length >= 2)
    # 		.MustAsync(async (x, c) => x == "foo")

    # 	self._validator.rule_for(lambda x: x.CreditCard)
    # 		.MustAsync(async (x, c) => x != null)
    # 		.MustAsync(async (x, c) => x.length >= 2)
    # 		.MustAsync(async (x, c) => x == "foo")

    # 	result = await self._validator.ValidateAsync(Person( Surname = "x", Forename = "x", Email = "x", CreditCard = "x" ))
    # 	self.assertEqual(len(result.errors),4)

    # async def test_Validation_stops_after_first_rule_when_first_rule_fails_and_globaldefault_class_Stop_async(self):
    # 	ValidatorOptions.Global.DefaultClassLevelCascadeMode = CascadeMode.Stop

    # 	self._validator.rule_for(lambda x: x.Surname)
    # 		.MustAsync(async (x, c) => x != null)
    # 		.MustAsync(async (x, c) => x.length >= 2)
    # 		.MustAsync(async (x, c) => x == "foo")

    # 	self._validator.rule_for(lambda x: x.Forename)
    # 		.MustAsync(async (x, c) => x != null)
    # 		.MustAsync(async (x, c) => x.length >= 2)
    # 		.MustAsync(async (x, c) => x == "foo")

    # 	self._validator.rule_for(lambda x: x.Email)
    # 		.MustAsync(async (x, c) => x != null)
    # 		.MustAsync(async (x, c) => x.length >= 2)
    # 		.MustAsync(async (x, c) => x == "foo")

    # 	self._validator.rule_for(lambda x: x.CreditCard)
    # 		.MustAsync(async (x, c) => x != null)
    # 		.MustAsync(async (x, c) => x.length >= 2)
    # 		.MustAsync(async (x, c) => x == "foo")

    # 	result = await self._validator.ValidateAsync(Person( Surname = "x", Forename = "x", Email = "x", CreditCard = "x" ))
    # 	self.assertEqual(len(result.errors),2)

    # async def test_Validation_stops_on_first_failure_when_classlevel_Stop_and_ruleleveldefault_Stop_async(self):
    # 	self.SetBothValidatorCascadeModes(CascadeMode.Stop)

    # 	self._validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self._validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_stops_on_first_failure_when_ruleleveldefault_Stop_async(self):
    # 	self._validator.RuleLevelCascadeMode = CascadeMode.Stop

    # 	self._validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_continues_when_classlevel_Continue_and_ruleleveldefault_Continue_async(self):
    # 	self.SetBothValidatorCascadeModes(CascadeMode.Continue)

    # 	self._validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 2)

    # async def test_Validation_continues_on_failure_when_classlevel_Stop_and_ruleleveldefault_Stop_and_ruleleveloverride_Continue_async(self):
    # 	self.SetBothValidatorCascadeModes(CascadeMode.Stop)

    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 2)

    # async def test_Validation_continues_on_failure_when_ruleleveldefault_Stop_and_ruleleveloverride_Continue_async(self):
    # 	self._validator.RuleLevelCascadeMode = CascadeMode.Stop

    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 2)

    # async def test_Validation_stops_on_failure_when_classlevel_Continue_and_ruleleveldefault_Continue_and_ruleleveloverride_Stop_async(self):
    # 	self.SetBothValidatorCascadeModes(CascadeMode.Continue)

    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_stops_on_failure_when_classlevel_Continue_and_ruleleveldefault_Continue_and_ruleleveloverride_Stop_async_legacy(self):
    # 	self.SetBothValidatorCascadeModes(CascadeMode.Continue)

    # 	self._validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.StopOnFirstFailure).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Cascade_mode_can_be_set_after_validator_instantiated_async(self):
    # 	self._validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self.SetBothValidatorCascadeModes(CascadeMode.Stop)
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Cascade_mode_can_be_set_after_validator_instantiated_async_legacy(self):
    # 	self._validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self._validator.RuleLevelCascadeMode = CascadeMode.Stop
    # 	results = await self._validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Cascade_set_to_stop_in_child_validator_with_RuleForEach_in_parent(self):
    # 	# See https://github.com/p-hzamora/FluentValidation/issues/2207

    # 	childValidator = InlineValidator[Order](Order)
    # 	childValidator.ClassLevelCascadeMode = CascadeMode.Stop
    # 	childValidator.rule_for(lambda x: x.ProductName).not_null()
    # 	childValidator.rule_for(lambda x: x.Amount).GreaterThan(0)

    # 	parentValidator = InlineValidator<Person>()
    # 	parentValidator.RuleForEach(lambda x: x.Orders).SetValidator(childValidator)

    # 	testData = list[Order] {
    # 		# Would cause both rules to fail, but only first rule will be executed because of CascadeMode.Stop
    # 		Order { ProductName = null, Amount = 0 },

    # 		# First rule succeeds, second rule fails.
    # 		Order { ProductName = "foo", Amount = 0 }

    # 	# Bug in #2207 meant that the rule for Orders[1].Amount would never execute
    # 	# as the cascade mode logic was stopping if totalFailures > 0 rather than totalFailures > (count of failures before rule executed)
    # 	result = parentValidator.validate(Person(Orders = testData))
    # 	self.assertEqual(len(result.errors),2)
    # 	result.Errors[0].PropertyName.ShouldEqual("Orders[0].ProductName")
    # 	result.Errors[1].PropertyName.ShouldEqual("Orders[1].Amount")

    def SetBothValidatorCascadeModes(self, cascadeMode: CascadeMode) -> None:
        self._validator.ClassLevelCascadeMode = cascadeMode
        self._validator.RuleLevelCascadeMode = cascadeMode

    @staticmethod
    def SetBothGlobalCascadeModes(cascadeMode: CascadeMode) -> None:
        ValidatorOptions.Global.DefaultClassLevelCascadeMode = cascadeMode
        ValidatorOptions.Global.DefaultRuleLevelCascadeMode = cascadeMode


if __name__ == "__main__":
    unittest.main()
