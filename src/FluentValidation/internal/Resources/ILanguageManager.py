from abc import ABC, abstractmethod
import locale
from typing import overload

from ..ExtensionInternal import ExtensionsInternal


class CultureInfo:
    CurrentUICulture = None

    @overload
    def __new__(cls) -> None:
        ...

    @overload
    def __new__(cls, curent_ui_Culture) -> None:
        ...

    def __new__(cls, current_ui_Culture=None) -> None:
        if current_ui_Culture is None:
            cls.CurrentUICulture, _ = locale.getdefaultlocale()
        else:
            cls.CurrentUICulture = current_ui_Culture


class ILanguageManager(ABC, ExtensionsInternal):
    @property
    @abstractmethod
    def Enabled(self) -> bool:
        ...

    @property
    @abstractmethod
    def Culture(self) -> CultureInfo:
        ...

    @abstractmethod
    def GetString(self, key: str, culture: CultureInfo = None):
        ...
