class Order:

    def __init__(self, id, name, address, price, currency):
        self.id = id
        self.name = name
        self.address = address
        self.price = price
        self.currency = currency

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            address=data["address"],
            price=data["price"],
            currency=data["currency"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "price": self.price,
            "currency": self.currency
        }
