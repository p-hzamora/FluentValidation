class IndonesianLanguage:
    Culture: str = "id"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' bukan alamat email yang benar.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' harus lebih besar dari atau sama dengan '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' harus lebih besar dari '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' harus di antara {min_length} dan {max_length} karakter. Anda memasukkan {total_length} karakter.",
            "MinimumLengthValidator": "Panjang dari '{PropertyName}' harus paling tidak {min_length} karakter. Anda memasukkan {total_length} karakter.",
            "MaximumLengthValidator": "Panjang dari '{PropertyName}' harus {max_length} karakter atau kurang. Anda memasukkan {total_length} karakter.",
            "LessThanOrEqualValidator": "'{PropertyName}' harus kurang dari atau sama dengan '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' harus kurang dari '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' tidak boleh kosong.",
            "NotEqualValidator": "'{PropertyName}' tidak boleh sama dengan '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' tidak boleh kosong.",
            "PredicateValidator": "Kondisi yang ditentukan tidak terpenuhi untuk '{PropertyName}'.",
            "AsyncPredicateValidator": "Kondisi yang ditentukan tidak terpenuhi untuk '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' bukan dalam format yang benar.",
            "EqualValidator": "'{PropertyName}' harus sama dengan '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' harus {max_length} karakter panjangnya. Anda memasukkan {total_length} karakter.",
            "InclusiveBetweenValidator": "'{PropertyName}' harus di antara {From} dan {To}. Anda memasukkan {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' harus di antara {From} dan {To} (exclusive). Anda memasukkan {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' bukan nomor kartu kredit yang benar.",
            "ScalePrecisionValidator": "Jumlah digit '{PropertyName}' tidak boleh lebih dari {ExpectedPrecision}, dengan toleransi {ExpectedScale} desimal. {Digits} digit dan {ActualScale} desimal ditemukan.",
            "EmptyValidator": "'{PropertyName}' harus kosong.",
            "NullValidator": "'{PropertyName}' harus kosong.",
            "EnumValidator": "'{PropertyName}' memiliki rentang nilai yang tidak mengikutsertakan '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' harus di antara {min_length} dan {max_length} karakter.",
            "MinimumLength_Simple": "Panjang dari '{PropertyName}' harus paling tidak {min_length} karakter.",
            "MaximumLength_Simple": "Panjang dari '{PropertyName}' harus {max_length} karakter atau fewer.",
            "ExactLength_Simple": "'{PropertyName}' harus {max_length} karakter panjangnya.",
            "InclusiveBetween_Simple": "'{PropertyName}' harus di antara {From} dan {To}.",
        }
        return dicc.get(key, None)
