from models.order import Order
from services.interfaces import ICurrencyTransformer

class CurrencyTransformer(ICurrencyTransformer):

    def transform(self, order: Order, currency: str, exchange_rate: str) -> Order:
        """貨幣轉換
        
        :param order: 訂單
        :param currency: 轉換後的貨幣
        :param exchange_rate: 貨幣匯率

        :return: 轉換後的訂單
        """
        order.price = int(order.price) * int(exchange_rate)
        order.currency = currency
        order.price = str(order.price)
        return order