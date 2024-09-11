from fluent_validation.internal.Resources.ILanguageManager import CultureInfo


class CultureScope:
    CurrentCulture: CultureInfo = None

    @classmethod
    def SetDefaultCulture(cls):
        cls.CurrentCulture = CultureInfo("en-US")
