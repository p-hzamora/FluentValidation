class ChineseTraditionalLanguage:
    Culture: str = "zh-Hant"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' 不是有效的電子郵件地址。",
            "GreaterThanOrEqualValidator": "'{PropertyName}' 必須大於或等於 '{ComparisonValue}'。",
            "GreaterThanValidator": "'{PropertyName}' 必須大於 '{ComparisonValue}'。",
            "LengthValidator": "'{PropertyName}' 的長度必須在 {min_length} 到 {max_length} 字符，您輸入了 {total_length} 字符。",
            "MinimumLengthValidator": "'{PropertyName}' 必須大於或等於{min_length}個字符。您輸入了{total_length}個字符。",
            "MaximumLengthValidator": "'{PropertyName}' 必須小於或等於{max_length}個字符。您輸入了{total_length}個字符。",
            "LessThanOrEqualValidator": "'{PropertyName}' 必須小於或等於 '{ComparisonValue}'。",
            "LessThanValidator": "'{PropertyName}' 必須小於 '{ComparisonValue}'。",
            "NotEmptyValidator": "'{PropertyName}' 不能為空。",
            "NotEqualValidator": "'{PropertyName}' 不能和 '{ComparisonValue}' 相等。",
            "NotNullValidator": "'{PropertyName}' 不能為Null。",
            "PredicateValidator": "'{PropertyName}' 不符合指定的條件。",
            "AsyncPredicateValidator": "'{PropertyName}' 不符合指定的條件。",
            "RegularExpressionValidator": "'{PropertyName}' 的格式不正確。",
            "EqualValidator": "'{PropertyName}' 應該和 '{ComparisonValue}' 相等。",
            "ExactLengthValidator": "'{PropertyName}' 必須是 {max_length} 個字符，您輸入了 {total_length} 字符。",
            "InclusiveBetweenValidator": "'{PropertyName}' 必須在 {From} (包含)和 {To} (包含)之間， 您輸入了 {PropertyValue}。",
            "ExclusiveBetweenValidator": "'{PropertyName}' 必須在 {From} (不包含)和 {To} (不包含)之間， 您輸入了 {PropertyValue}。",
            "CreditCardValidator": "'{PropertyName}' 不是有效的信用卡號碼。",
            "ScalePrecisionValidator": "'{PropertyName}' 總位數不能超過 {ExpectedPrecision} 位，其中小數部份 {ExpectedScale} 位。您共計輸入了 {Digits} 位數字，其中小數部份{ActualScale} 位。",
            "EmptyValidator": "'{PropertyName}' 必須為空。",
            "NullValidator": "'{PropertyName}' 必須為Null。",
            "EnumValidator": "'{PropertyName}' 的數值範圍不包含 '{PropertyValue}'。",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' 的長度必須在 {min_length} 到 {max_length} 字符。",
            "MinimumLength_Simple": "'{PropertyName}' 必須大於或等於{min_length}個字符。",
            "MaximumLength_Simple": "'{PropertyName}' 必須小於或等於{max_length}個字符。",
            "ExactLength_Simple": "'{PropertyName}' 必須是 {max_length} 個字符。",
            "InclusiveBetween_Simple": "'{PropertyName}' 必須在 {From} (包含)和 {To} (包含)之間。",
        }
        return dicc.get(key, None)
