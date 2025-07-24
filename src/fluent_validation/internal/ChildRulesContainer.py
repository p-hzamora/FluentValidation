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

from typing import Callable
from fluent_validation.InlineValidator import InlineValidator
from fluent_validation.syntax import IRuleBuilderOptions


class ChildRulesContainer[T](InlineValidator[T]):
    """
    /// AbstractValidator implementation for containing child rules.
    """

    def __init__[TProperty](self, model: type[T] | None, *ruleCreator: Callable[[InlineValidator[T]], IRuleBuilderOptions[T, TProperty]]) -> None:
        super().__init__(model, *ruleCreator)
        self._RuleSetsToApplyToChildRules: list[str] = None

    @property
    def RuleSetsToApplyToChildRules(self) -> list[str]:
        """
        Used to keep track of rulesets from parent that need to be applied
        to child rules in the case of multiple nested child rules.
        """
        # cref="DefaultValidatorExtensions.child_rules{T,TProperty}"
        return self._RuleSetsToApplyToChildRules

    @RuleSetsToApplyToChildRules.setter
    def RuleSetsToApplyToChildRules(self, value: list[str]):
        self._RuleSetsToApplyToChildRules = value
