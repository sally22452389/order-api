from models.order import Order
from services.consts import *
from services.interfaces import IChecking, ICurrencyTransformer

class OrderService:

    def __init__(self, checking_service: IChecking, currency_transformer: ICurrencyTransformer):
        self.checking = checking_service
        self.currency_transformer = currency_transformer

    def process_order(self, data: dict) -> dict:
        """處理訂單格式檢查與轉換
        
        :param data: 訂單資料

        :return: 處理後的訂單資料

        :raises ValidationError: 訂單資料格式錯誤
        """
        # 建立成物件
        order = Order.from_dict(data)

        # 訂單格式檢查
        self.checking.checking_order(order)

        # 貨幣轉換
        if order.currency == USD:
            order = self.currency_transformer.transform(order, TWD, EXCHANGE_RATE)

        return order.to_dict()
