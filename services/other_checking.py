from services.interfaces import IChecking
from models.order import Order
from services.checking import Checking  

class OtherChecking(Checking):

    def checking_order(self, order: Order) -> None:
        super().checking_order(order)
        self.check_address(order.address)
    
    def check_address(self, address) -> None:
        pass
    