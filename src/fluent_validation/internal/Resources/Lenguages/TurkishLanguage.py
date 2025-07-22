class TurkishLanguage:
    Culture: str = "tr"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}'  geçerli bir e-posta adresi değil.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' değeri '{ComparisonValue}' değerinden büyük veya eşit olmalı.",
            "GreaterThanValidator": "'{PropertyName}' değeri '{ComparisonValue}' değerinden büyük olmalı.",
            "LengthValidator": "'{PropertyName}', {min_length} ve {max_length} arasında karakter uzunluğunda olmalı . Toplam {total_length} adet karakter girdiniz.",
            "MinimumLengthValidator": "'{PropertyName}', {min_length} karakterden büyük veya eşit olmalıdır. {total_length} karakter girdiniz.",
            "MaximumLengthValidator": "'{PropertyName}', {max_length} karakterden küçük veya eşit olmalıdır. {total_length} karakter girdiniz.",
            "LessThanOrEqualValidator": "'{PropertyName}', '{ComparisonValue}' değerinden küçük veya eşit olmalı.",
            "LessThanValidator": "'{PropertyName}', '{ComparisonValue}' değerinden küçük olmalı.",
            "NotEmptyValidator": "'{PropertyName}' boş olmamalı.",
            "NotEqualValidator": "'{PropertyName}', '{ComparisonValue}' değerine eşit olmamalı.",
            "NotNullValidator": "'{PropertyName}' boş olamaz.",
            "PredicateValidator": "Belirtilen durum '{PropertyName}' için geçerli değil.",
            "AsyncPredicateValidator": "Belirtilen durum '{PropertyName}' için geçerli değil.",
            "RegularExpressionValidator": "'{PropertyName}' değerinin formatı doğru değil.",
            "EqualValidator": "'{PropertyName}', '{ComparisonValue}' değerine eşit olmalı.",
            "ExactLengthValidator": "'{PropertyName}', {max_length} karakter uzunluğunda olmalı. {total_length} adet karakter girdiniz.",
            "InclusiveBetweenValidator": "'{PropertyName}', {From} ve {To} arasında olmalı. {PropertyValue} değerini girdiniz.",
            "ExclusiveBetweenValidator": "'{PropertyName}', {From} ve {To} (dahil değil) arasında olmalı. {PropertyValue} değerini girdiniz.",
            "CreditCardValidator": "'{PropertyName}' geçerli bir kredi kartı numarası değil.",
            "ScalePrecisionValidator": "'{PropertyName}', {ExpectedScale} ondalıkları için toplamda {ExpectedPrecision} rakamdan fazla olamaz. {Digits} basamak ve {ActualScale} basamak bulundu.",
            "EmptyValidator": "'{PropertyName}' boş olmalıdır.",
            "NullValidator": "'{PropertyName}' boş olmalıdır.",
            "EnumValidator": "'{PropertyName}', '{PropertyValue}' içermeyen bir değer aralığı içeriyor.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}', {min_length} ve {max_length} arasında karakter uzunluğunda olmalı.",
            "MinimumLength_Simple": "'{PropertyName}', {min_length} karakterden büyük veya eşit olmalıdır.",
            "MaximumLength_Simple": "'{PropertyName}', {max_length} karakterden küçük veya eşit olmalıdır.",
            "ExactLength_Simple": "'{PropertyName}', {max_length} karakter uzunluğunda olmalı.",
            "InclusiveBetween_Simple": "'{PropertyName}', {From} ve {To} arasında olmalı.",
        }
        return dicc.get(key, None)