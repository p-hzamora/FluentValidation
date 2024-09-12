from abc import ABC, abstractmethod
import locale
from typing import overload

from fluent_validation.internal.ExtensionInternal import ExtensionsInternal


class CultureInfo:
    CurrentUICulture = None

    @overload
    def __new__(cls) -> "CultureInfo": ...

    @overload
    def __new__(cls, curent_ui_Culture) -> "CultureInfo": ...

    def __new__(cls, current_ui_Culture=None) -> "CultureInfo":
        if current_ui_Culture is None:
            cls.CurrentUICulture, _ = locale.getlocale()
        elif not CultureInfo.CurrentUICulture:
            cls.CurrentUICulture = current_ui_Culture
        return object.__new__(cls)


class ILanguageManager(ABC, ExtensionsInternal):
    @property
    @abstractmethod
    def Enabled(self) -> bool: ...

    @property
    @abstractmethod
    def Culture(self) -> CultureInfo: ...

    @abstractmethod
    def GetString(self, key: str, culture: CultureInfo = None): ...
