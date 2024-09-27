from abc import ABC, abstractmethod
from models.order import Order

class IChecking(ABC):
    @abstractmethod
    def checking_order(self, order: Order) -> None:
        pass

class ICurrencyTransformer(ABC):
    @abstractmethod
    def transform(self, order: Order, currency: str, exchange_rate: str) -> Order:
        pass