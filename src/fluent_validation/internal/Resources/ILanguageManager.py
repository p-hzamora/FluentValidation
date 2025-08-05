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
from abc import ABC, abstractmethod
import locale
import threading
from typing import ClassVar, Optional, Protocol, overload, TYPE_CHECKING

from fluent_validation.internal.ExtensionInternal import ExtensionsInternal


class CurrentThreadType(Protocol):
    CurrentCulture: CultureInfo
    CurrentUICulture: CultureInfo


_language_map_similarity: dict[str, str] = {
    "zh-CN": "zh-Hans",
    "zh-SG": "zh-Hans",
}
_thread_culture: CurrentThreadType = threading.local()

HYPHEN = "-"


def get_default_ui() -> str:
    """Get the default UI culture from system locale"""
    # getlocale() method should always return a tuple of two elements
    loc = locale.getlocale()[0] or "en-US"
    return loc.replace("_", HYPHEN)


class CultureInfo:
    """Python implementation of .NET CultureInfo class"""

    # Class variables for cached instances
    _current_ui_culture: ClassVar[Optional[CultureInfo]] = None
    _invariant_culture: ClassVar[Optional[CultureInfo]] = None

    @overload
    def __init__(self): ...

    @overload
    def __init__(self, culture_name: str): ...

    def __init__(self, culture_name: Optional[str] = None):
        self._name = get_default_ui() if culture_name is None else culture_name

    @property
    def Name(self) -> str:
        """Gets the culture name"""
        return self._name

    @property
    def TwoLettersISOLanguage(self) -> str:
        if HYPHEN in self.Name and self.Name:
            return self.Name.split(HYPHEN)[0]
        return self.Name

    @property
    def Parent(self) -> CultureInfo:
        """Gets the parent culture (language without region)"""

        if self.Name in _language_map_similarity:
            return CultureInfo(_language_map_similarity[self.Name])

        if HYPHEN in self.Name and self.Name:
            parent_name = self.Name.split(HYPHEN)[:-1]

            return CultureInfo("-".join(parent_name))

        # If already neutral or empty, return invariant culture
        return CultureInfo.InvariantCulture()

    @property
    def IsNeutralCulture(self) -> bool:
        """True if no region specified (e.g. 'es' is neutral, 'es-MX' is not)"""
        return HYPHEN not in self.Name and self.Name != ""

    @classmethod
    def CurrentUICulture(cls) -> CultureInfo:
        """Gets the current UI culture (cached)"""
        if hasattr(_thread_culture, "CurrentUICulture"):
            return _thread_culture.CurrentUICulture
        return CultureInfo(get_default_ui())

    @classmethod
    def set_current_ui_culture(cls, culture: CultureInfo) -> None:
        """Sets the current UI culture"""
        cls._current_ui_culture = culture

    @classmethod
    def InvariantCulture(cls) -> CultureInfo:
        """Gets the invariant culture (cached)"""
        if cls._invariant_culture is None:
            cls._invariant_culture = CultureInfo("")
        return cls._invariant_culture

    def __eq__(self, other) -> bool:
        """Check equality based on culture name"""
        return isinstance(other, CultureInfo) and self.Name == other.Name

    def __hash__(self) -> int:
        """Make CultureInfo hashable"""
        return hash(self.Name)

    def __repr__(self) -> str:
        return f"CultureInfo('{self.Name}')"

    def __str__(self) -> str:
        return self.Name


class ILanguageManager(ABC, ExtensionsInternal):
    @property
    @abstractmethod
    def Enabled(self) -> bool: ...

    @property
    @abstractmethod
    def Culture(self) -> CultureInfo: ...

    @overload
    def GetString(self, key: str) -> str: ...
    @overload
    def GetString(self, key: str, culture: CultureInfo) -> str: ...
    @abstractmethod
    def GetString(self, key: str, culture: Optional[CultureInfo] = None) -> str:
        """
        Gets a translated string based on its key. If the culture is specific and it isn't registered, we try the neutral culture instead.
        If no matching culture is found  to be registered we use English.

        Args:
            key: The key
            culture: The culture to translate into

        Return:
            str

        """
        ...

    if TYPE_CHECKING:

        def ResolveErrorMessageUsingErrorCode(languageManager: ILanguageManager, error_code: str, fall_back_Key: str) -> str: ...
