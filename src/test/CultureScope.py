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

from typing import ClassVar
from fluent_validation.internal.Resources.ILanguageManager import CultureInfo, _thread_culture


class CultureScope:
    _originalUiCulture: ClassVar[CultureInfo]
    _originalCulture: ClassVar[CultureInfo]

    def __init__(self, culture: CultureInfo | str):
        if isinstance(culture, str):
            self.__init__(CultureInfo(culture))
            return None

        self.initialize_thread()
        self._originalCulture = _thread_culture.CurrentCulture
        self._originalUiCulture = _thread_culture.CurrentUICulture

        _thread_culture.CurrentCulture = culture
        _thread_culture.CurrentUICulture = culture

    @staticmethod
    def SetDefaultCulture():
        _thread_culture.CurrentCulture = CultureInfo("en-US")
        _thread_culture.CurrentUICulture = CultureInfo("en-US")

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        _thread_culture.CurrentCulture = self._originalCulture
        _thread_culture.CurrentUICulture = self._originalUiCulture

    def initialize_thread(self) -> None:
        self.SetDefaultCulture()

    def set_CurrentCulture(self, value: CultureInfo) -> None:
        _thread_culture.CurrentCulture = value

    def set_CurrentUICulture(self, value: CultureInfo) -> None:
        _thread_culture.CurrentUICulture = value
