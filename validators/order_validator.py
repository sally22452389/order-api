from validators.consts import *
from exceptions.order_exceptions import ValidationError

class OrderValidator:

    def validate(self, data: dict) -> None: 
        """檢查訂單資料的必要欄位和型別是否正確
        
        :param data: 訂單資料

        :raises ValidationError: 訂單資料錯誤
        """
        required_fields = {
            "id": str,
            "name": str,
            "address": dict,
            "price": str,
            "currency": str
        }

        for field, expected_type in required_fields.items():
            if field not in data:
                raise ValidationError(MISSING_REQUIRED_FIELD.format(field=field))
            if not isinstance(data[field], expected_type):
                raise ValidationError(INVALID_FIELD_TYPE.format(field=field, expected_type=expected_type.__name__))

        address_required_fields = {
            "city": str,
            "district": str,
            "street": str
        }

        address = data.get("address")
        for field, expected_type in address_required_fields.items():
            if field not in address:
                raise ValidationError(MISSING_REQUIRED_FIELD.format(field=f"address {field}"))
            if not isinstance(address[field], expected_type):
                raise ValidationError(INVALID_FIELD_TYPE.format(field=f"address {field}", expected_type=expected_type.__name__))