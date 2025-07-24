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

from __future__ import annotations
from typing import Iterable, override, TYPE_CHECKING

from fluent_validation.internal.IValidatorSelector import IValidatorSelector

if TYPE_CHECKING:
    from fluent_validation.IValidationContext import IValidationContext
    from fluent_validation.IValidationRule import IValidationRule


class CompositeValidatorSelector(IValidatorSelector):
    def __init__(self, selectors: Iterable[IValidatorSelector]):
        self._selectors: Iterable[IValidatorSelector] = selectors

    @override
    def CanExecute(self, rule: IValidationRule, propertyPath: str, context: IValidationContext) -> bool:
        return any([s.CanExecute(rule, propertyPath, context) for s in self._selectors])
