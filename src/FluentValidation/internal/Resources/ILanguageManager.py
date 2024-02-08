from abc import ABC, abstractmethod
import locale  # noqa: F401

from ..ExtensionInternal import ExtensionsInternal


class CultureInfo:
    CurrentUICulture, _ = ("en-US", "__")  # locale.getdefaultlocale()


class ILanguageManager(ABC, ExtensionsInternal):
    @property
    @abstractmethod
    def Enabled(sefl) -> bool:
        ...

    @property
    @abstractmethod
    def Culture(sefl) -> CultureInfo:
        ...

    @abstractmethod
    def GetString(sefl, key: str, culture: CultureInfo = None):
        ...
