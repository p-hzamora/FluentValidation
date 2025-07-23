import unittest
import sys
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation import ValidatorOptions, CascadeMode

from fluent_validation.internal.TrackingCollection import IDisposable
from TestValidator import TestValidator


class CascadeModePropertiesTesterLegacy(unittest.TestCase, IDisposable):
    def setUp(self):
        self.SetBothGlobalCascadeModes(CascadeMode.Continue)
        self._validator: TestValidator = TestValidator()

    def tearDown(self) -> None:
        ValidatorOptions.Global.DefaultClassLevelCascadeMode = CascadeMode.Continue
        ValidatorOptions.Global.DefaultRuleLevelCascadeMode = CascadeMode.Continue

    def Dispose(self):
        self.SetBothGlobalCascadeModes(CascadeMode.Continue)

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, *args, **kwargs):
        return self.Dispose()

    def test_Setting_global_default_CascadeMode_Stop_sets_both_rule_and_class_level_global_default_properties(self) -> None:
        ValidatorOptions.Global.CascadeMode = CascadeMode.Stop

        self.assertEqual(CascadeMode.Stop, ValidatorOptions.Global.DefaultRuleLevelCascadeMode)
        self.assertEqual(CascadeMode.Stop, ValidatorOptions.Global.DefaultClassLevelCascadeMode)

    def test_Setting_global_default_CascadeMode_Continue_sets_both_rule_and_class_level_global_default_properties(self) -> None:
        ValidatorOptions.Global.CascadeMode = CascadeMode.Stop
        ValidatorOptions.Global.CascadeMode = CascadeMode.Continue

        self.assertEqual(CascadeMode.Continue, ValidatorOptions.Global.DefaultRuleLevelCascadeMode)
        self.assertEqual(CascadeMode.Continue, ValidatorOptions.Global.DefaultClassLevelCascadeMode)

    # def test_Setting_global_default_CascadeMode_StopOnFirstFailure_sets_rule_Stop_and_class_Continue(self)->None:
    # # 	ValidatorOptions.Global.CascadeMode = CascadeMode.StopOnFirstFailure

    # # 	self.assertEqual(CascadeMode.Stop, ValidatorOptions.Global.DefaultRuleLevelCascadeMode)
    # # 	self.assertEqual(CascadeMode.Continue, ValidatorOptions.Global.DefaultClassLevelCascadeMode)

    def test_Setting_class_CascadeMode_Stop_sets_both_rule_and_class_level_properties(self) -> None:
        self._validator.CascadeMode = CascadeMode.Stop

        self.assertEqual(CascadeMode.Stop, self._validator.RuleLevelCascadeMode)
        self.assertEqual(CascadeMode.Stop, self._validator.ClassLevelCascadeMode)

    def test_Setting_class_CascadeMode_Continue_sets_both_rule_and_class_level_properties(self) -> None:
        self._validator.CascadeMode = CascadeMode.Stop
        self._validator.CascadeMode = CascadeMode.Continue

        self.assertEqual(CascadeMode.Continue, self._validator.RuleLevelCascadeMode)
        self.assertEqual(CascadeMode.Continue, self._validator.ClassLevelCascadeMode)

    # def test_Setting_class_CascadeMode_StopOnFirstFailure_sets_rule_Stop_and_class_Continue(self) -> None:
    # self._validator.CascadeMode = CascadeMode.StopOnFirstFailure

    # self.assertEqual(CascadeMode.Stop, self._validator.RuleLevelCascadeMode)
    # self.assertEqual(CascadeMode.Continue, self._validator.ClassLevelCascadeMode)

    # def test_Setting_global_DefaultRuleLevelCascadeMode_to_StopOnFirstFailure_sets_Stop(self) -> None:
    # ValidatorOptions.Global.DefaultRuleLevelCascadeMode = CascadeMode.StopOnFirstFailure

    # self.assertEqual(CascadeMode.Stop, ValidatorOptions.Global.DefaultRuleLevelCascadeMode)

    # def test_Setting_global_DefaultClassLevelCascadeMode_to_StopOnFirstFailure_sets_Stop(self) -> None:
    # ValidatorOptions.Global.DefaultClassLevelCascadeMode = CascadeMode.StopOnFirstFailure

    # self.assertEqual(CascadeMode.Stop, ValidatorOptions.Global.DefaultClassLevelCascadeMode)

    # def test_Setting_class_RuleLevelCascadeMode_to_StopOnFirstFailure_sets_Stop(self) -> None:
    # self._validator.RuleLevelCascadeMode = CascadeMode.StopOnFirstFailure

    # self.assertEqual(CascadeMode.Stop, self._validator.RuleLevelCascadeMode)

    # def test_Setting_class_ClassLevelCascadeMode_to_StopOnFirstFailure_sets_Stop(self) -> None:
    # self._validator.ClassLevelCascadeMode = CascadeMode.StopOnFirstFailure

    # self.assertEqual(CascadeMode.Stop, self._validator.ClassLevelCascadeMode)

    def test_Global_default_CascadeMode_Get_returns_Stop_when_both_Stop(self) -> None:
        self.SetBothGlobalCascadeModes(CascadeMode.Stop)

        self.assertEqual(CascadeMode.Stop, ValidatorOptions.Global.CascadeMode)

    def test_Global_default_CascadeMode_Get_returns_Continue_when_both_Continue(self) -> None:
        self.SetBothGlobalCascadeModes(CascadeMode.Stop)
        self.SetBothGlobalCascadeModes(CascadeMode.Continue)

        self.assertEqual(CascadeMode.Continue, ValidatorOptions.Global.CascadeMode)

    # def test_Global_default_CascadeMode_Get_returns_StopOnFirstFailure_when_class_Continue_and_rule_Stop(self) -> None:
    #     ValidatorOptions.Global.DefaultClassLevelCascadeMode = CascadeMode.Continue
    #     ValidatorOptions.Global.DefaultRuleLevelCascadeMode = CascadeMode.Stop

    #     self.assertEqual(CascadeMode.StopOnFirstFailure, ValidatorOptions.Global.CascadeMode)

    def test_Global_default_CascadeMode_Get_throws_exception_when_class_Stop_and_rule_Continue(self) -> None:
        ValidatorOptions.Global.DefaultClassLevelCascadeMode = CascadeMode.Stop
        ValidatorOptions.Global.DefaultRuleLevelCascadeMode = CascadeMode.Continue

        with self.assertRaises(Exception):
            ValidatorOptions.Global.CascadeMode

    def test_Class_CascadeMode_Get_returns_Stop_when_both_Stop(self) -> None:
        self.SetBothValidatorCascadeModes(CascadeMode.Stop)

        self.assertEqual(CascadeMode.Stop, self._validator.CascadeMode)

    def test_Class_CascadeMode_Get_returns_Continue_when_both_Continue(self) -> None:
        self.SetBothValidatorCascadeModes(CascadeMode.Stop)
        self.SetBothValidatorCascadeModes(CascadeMode.Continue)

        self.assertEqual(CascadeMode.Continue, self._validator.CascadeMode)

    def test_Class_CascadeMode_Get_returns_StopOnFirstFailure_when_class_Continue_and_rule_Stop(self) -> None:
        self._validator.ClassLevelCascadeMode = CascadeMode.Continue
        self._validator.RuleLevelCascadeMode = CascadeMode.Stop

    #     self.assertEqual(CascadeMode.StopOnFirstFailure, self._validator.CascadeMode)

    def test_Class_CascadeMode_Get_throws_exception_when_class_Stop_and_rule_Continue(self) -> None:
        self._validator.ClassLevelCascadeMode = CascadeMode.Stop
        self._validator.RuleLevelCascadeMode = CascadeMode.Continue

        with self.assertRaises(Exception):
            self._validator.CascadeMode

    def SetBothValidatorCascadeModes(self, cascadeMode: CascadeMode) -> None:
        self._validator.ClassLevelCascadeMode = cascadeMode
        self._validator.RuleLevelCascadeMode = cascadeMode

    @staticmethod
    def SetBothGlobalCascadeModes(cascadeMode: CascadeMode) -> None:
        ValidatorOptions.Global.DefaultClassLevelCascadeMode = cascadeMode
        ValidatorOptions.Global.DefaultRuleLevelCascadeMode = cascadeMode


if __name__ == "__main__":
    unittest.main()
