from services.consts import *
from services.utils import is_valid_name, is_capitalize_first_letter
from services.interfaces import IChecking
from models.order import Order
from exceptions.order_exceptions import ValidationError

class Checking(IChecking):

    def checking_order(self, order: Order):
        """檢查訂單格式"""
        self.check_name(order.name)
        self.check_price(order.price)
        self.check_currency(order.currency)

    def check_name(self, name: str):
        if not is_valid_name(name):
            raise ValidationError(NAME_CONTAINS_NON_ENGLISH)
        if not is_capitalize_first_letter(name):
            raise ValidationError(NAME_NOT_CAPITALIZED)

    def check_price(self, price: str):
        if int(price) > 2000:
            raise ValidationError(PRICE_OVER_2000)

    def check_currency(self, currency: str):
        if currency not in [TWD, USD]:
            raise ValidationError(CURRENCY_FORMAT_IS_WRONG)