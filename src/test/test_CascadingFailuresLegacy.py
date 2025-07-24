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
from typing import override

from TestValidator import TestValidator
from person import Person


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())
from fluent_validation.internal.TrackingCollection import IDisposable
from fluent_validation import CascadeMode, ValidatorOptions


class CascadingFailuresTesterLegacy(unittest.TestCase, IDisposable):
    def setUp(self):
        ValidatorOptions.Global.CascadeMode = CascadeMode.Continue
        self.validator: TestValidator = TestValidator()

    def tearDown(self) -> None:
        ValidatorOptions.Global.CascadeMode = CascadeMode.Continue

    @override
    def Dispose(self):
        ValidatorOptions.Global.CascadeMode = CascadeMode.Continue

    @override
    def __enter__(self):
        return super().__enter__()

    @override
    def __exit__(self):
        return self.Dispose()

    def test_Validation_continues_on_failure(self):
        self.validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_stops_on_first_failure(self):
        ValidatorOptions.Global.CascadeMode = CascadeMode.Stop

        self.validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Validation_stops_on_first_failure_legacy(self):
        ValidatorOptions.Global.CascadeMode = CascadeMode.Stop

        self.validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Validation_continues_on_failure_when_set_to_Stop_globally_and_overriden_at_rule_level(self):
        ValidatorOptions.Global.CascadeMode = CascadeMode.Stop

        self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_continues_on_failure_when_set_to_Stop_globally_and_overriden_at_rule_level_legacy(self):
        ValidatorOptions.Global.CascadeMode = CascadeMode.Stop

        self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_stops_on_first_Failure_when_set_to_Continue_globally_and_overriden_at_rule_level(self):
        ValidatorOptions.Global.CascadeMode = CascadeMode.Continue
        self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Validation_stops_on_first_Failure_when_set_to_Continue_globally_and_overriden_at_rule_level_legacy(self):
        ValidatorOptions.Global.CascadeMode = CascadeMode.Continue
        self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Validation_continues_to_second_validator_when_first_validator_succeeds_and_cascade_set_to_stop(self):
        ValidatorOptions.Global.CascadeMode = CascadeMode.Stop
        self.validator.rule_for(lambda x: x.Surname).not_null().length(2, 10)
        result = self.validator.validate(Person(Surname="x"))
        self.assertFalse(result.is_valid)

    def test_Validation_continues_to_second_validator_when_first_validator_succeeds_and_cascade_set_to_stop_legacy(self):
        ValidatorOptions.Global.CascadeMode = CascadeMode.Stop
        self.validator.rule_for(lambda x: x.Surname).not_null().length(2, 10)
        result = self.validator.validate(Person(Surname="x"))
        self.assertFalse(result.is_valid)

    def test_Validation_stops_on_first_failure_when_set_to_StopOnFirstFailure_at_validator_level(self):
        self.validator.CascadeMode = CascadeMode.Stop

        self.validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        self.validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Validation_stops_on_first_failure_when_set_to_StopOnFirstFailure_at_validator_level_legacy(self):
        self.validator.CascadeMode = CascadeMode.Stop

        self.validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Validation_continues_when_set_to_Continue_at_validator_level(self):
        self.validator.CascadeMode = CascadeMode.Continue

        self.validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_continues_on_failure_when_set_to_Stop_at_validator_level_and_overriden_at_rule_level(self):
        self.validator.CascadeMode = CascadeMode.Stop

        self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_continues_on_failure_when_set_to_StopOnFirstFailure_at_validator_level_and_overriden_at_rule_level_legacy(self):
        self.validator.CascadeMode = CascadeMode.Stop

        self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 2)

    def test_Validation_stops_on_failure_when_set_to_Continue_and_overriden_at_rule_level(self):
        self.validator.CascadeMode = CascadeMode.Continue

        self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Validation_stops_on_failure_when_set_to_Continue_and_overriden_at_rule_level_legacy(self):
        self.validator.CascadeMode = CascadeMode.Continue

        self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).not_null().equal("Foo")
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Cascade_mode_can_be_set_after_validator_instantiated(self):
        self.validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        self.validator.CascadeMode = CascadeMode.Stop
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Cascade_mode_can_be_set_after_validator_instantiated_legacy(self):
        self.validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")
        self.validator.CascadeMode = CascadeMode.Stop
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    # async def test_Validation_continues_on_failure_async(self)->Awaitable:
    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors),2)

    # async def test_Validation_stops_on_first_failure_async(self)->Awaitable:
    # 	ValidatorOptions.Global.CascadeMode = CascadeMode.Stop

    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_stops_on_first_failure_async_legacy(self)->Awaitable:
    # 	ValidatorOptions.Global.CascadeMode = CascadeMode.Stop

    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_continues_on_failure_when_set_to_Stop_globally_and_overriden_at_rule_level_async(self)->Awaitable:
    # 	ValidatorOptions.Global.CascadeMode = CascadeMode.Stop

    # 	self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors),2)

    # async def test_Validation_continues_on_failure_when_set_to_Stop_globally_and_overriden_at_rule_level_async_legacy(self)->Awaitable:
    # 	ValidatorOptions.Global.CascadeMode = CascadeMode.Stop

    # 	self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors),2)

    # async def test_Validation_stops_on_first_Failure_when_set_to_Continue_globally_and_overriden_at_rule_level_async(self)->Awaitable:
    # 	ValidatorOptions.Global.CascadeMode = CascadeMode.Continue
    # 	self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_stops_on_first_Failure_when_set_to_Continue_globally_and_overriden_at_rule_level_async_legacy(self)->Awaitable:
    # 	ValidatorOptions.Global.CascadeMode = CascadeMode.Continue
    # 	self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_stops_on_first_Failure_when_set_to_Continue_globally_and_overriden_at_rule_level_and_async_validator_is_invoked_synchronously(self)->Awaitable:
    # 	ValidatorOptions.Global.CascadeMode = CascadeMode.Continue
    # 	self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).not_null().equal("Foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_stops_on_first_Failure_when_set_to_Continue_globally_and_overriden_at_rule_level_and_async_validator_is_invoked_synchronously_legacy(self)->Awaitable:
    # 	ValidatorOptions.Global.CascadeMode = CascadeMode.Continue
    # 	self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).not_null().equal("Foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_continues_to_second_validator_when_first_validator_succeeds_and_cascade_set_to_stop_async(self)->Awaitable:
    # 	ValidatorOptions.Global.CascadeMode = CascadeMode.Stop
    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	result = await self.validator.ValidateAsync(Person {Surname = "x")
    # 	self.assertFalse(result.is_valid)

    # async def test_Validation_continues_to_second_validator_when_first_validator_succeeds_and_cascade_set_to_stop_async_legacy(self)->Awaitable:
    # 	ValidatorOptions.Global.CascadeMode = CascadeMode.Stop
    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	result = await self.validator.ValidateAsync(Person {Surname = "x")
    # 	self.assertFalse(result.is_valid)

    # async def test_Validation_stops_on_first_failure_when_set_to_StopOnFirstFailure_at_validator_level_async(self)->Awaitable:
    # 	self.validator.CascadeMode = CascadeMode.Stop

    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_stops_on_first_failure_when_set_to_StopOnFirstFailure_at_validator_level_async_legacy(self)->Awaitable:
    # 	self.validator.CascadeMode = CascadeMode.Stop

    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_continues_when_set_to_Continue_at_validator_level_async(self)->Awaitable:
    # 	self.validator.CascadeMode = CascadeMode.Continue

    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors),2)

    # async def test_Validation_continues_on_failure_when_set_to_StopOnFirstFailure_at_validator_level_and_overriden_at_rule_level_async(self)->Awaitable:
    # 	self.validator.CascadeMode = CascadeMode.Stop

    # 	self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors),2)

    # async def test_Validation_continues_on_failure_when_set_to_StopOnFirstFailure_at_validator_level_and_overriden_at_rule_level_async_legacy(self)->Awaitable:
    # 	self.validator.CascadeMode = CascadeMode.Stop

    # 	self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Continue).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors),2)

    # async def test_Validation_stops_on_failure_when_set_to_Continue_and_overriden_at_rule_level_async(self)->Awaitable:
    # 	self.validator.CascadeMode = CascadeMode.Continue

    # 	self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Validation_stops_on_failure_when_set_to_Continue_and_overriden_at_rule_level_async_legacy(self)->Awaitable:
    # 	self.validator.CascadeMode = CascadeMode.Continue

    # 	self.validator.rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Cascade_mode_can_be_set_after_validator_instantiated_async(self)->Awaitable:
    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self.validator.CascadeMode = CascadeMode.Stop
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)

    # async def test_Cascade_mode_can_be_set_after_validator_instantiated_async_legacy(self)->Awaitable:
    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, c) => x != null).MustAsync(async (x, c) => x == "foo")
    # 	self.validator.CascadeMode = CascadeMode.Stop
    # 	results = await self.validator.ValidateAsync(Person())
    # 	self.assertEqual(len(results.errors), 1)


if __name__ == "__main__":
    unittest.main()
