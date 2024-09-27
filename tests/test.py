from main import create_app
from controllers.consts import *
from services.consts import *
from validators.consts import *
import unittest
import json

class TestOrderService(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.testing = True
        self.client = app.test_client()
        self.valid_order = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "2000",
            "currency": TWD,
        }

    def test_success_order(self):
        response = self.client.post(API_ORDERS, data=json.dumps(self.valid_order), content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)
        
    def test_missing_field(self, field="city"):
        order = self.valid_order.copy()
        del order["address"][field]
        response = self.client.post(API_ORDERS, data=json.dumps(order), content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['msg'], MISSING_REQUIRED_FIELD.format(field=f"address {field}"))

    def test_wrong_type(self, price=2050):
        order = self.valid_order.copy()
        order["price"] = price
        response = self.client.post(API_ORDERS, data=json.dumps(order), content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['msg'], INVALID_FIELD_TYPE.format(field="price", expected_type="str"))

    def test_name_contains_non_english(self, name="melody holiday 酒店"):
        order = self.valid_order.copy()
        order["name"] = name
        response = self.client.post(API_ORDERS, data=json.dumps(order), content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['msg'], NAME_CONTAINS_NON_ENGLISH)

    def test_name_not_capitalized(self, name="melody holiday inn"):
        order = self.valid_order.copy()
        order["name"] = name
        response = self.client.post(API_ORDERS, data=json.dumps(order), content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['msg'], NAME_NOT_CAPITALIZED)

    def test_price_over_2000(self, price="2050"):
        order = self.valid_order.copy()
        order["price"] = price
        response = self.client.post(API_ORDERS, data=json.dumps(order), content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['msg'], PRICE_OVER_2000)

    def test_currency_wrong_format(self, currency="JPY"):
        order = self.valid_order.copy()
        order["currency"] = currency
        response = self.client.post(API_ORDERS, data=json.dumps(order), content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['msg'], CURRENCY_FORMAT_IS_WRONG)

    def test_currency_usd_conversion(self, price="50"):
        order = self.valid_order.copy()
        order["currency"] = USD
        order["price"] = price
        response = self.client.post(API_ORDERS, data=json.dumps(order), content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)
        self.assertEqual(response.json['data']["currency"], TWD)
        self.assertEqual(response.json['data']["price"], str(int(price) * int(EXCHANGE_RATE)))

if __name__ == "__main__":
    unittest.main()
