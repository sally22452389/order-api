from flask import Blueprint, request, jsonify
from controllers.consts import *
from validators.order_validator import OrderValidator
from services.order_service import OrderService
from services.checking import Checking
from services.currency_transformer import CurrencyTransformer
from exceptions.order_exceptions import ValidationError

order = Blueprint("order_api", __name__)

@order.route(API_ORDERS, methods=[POST])
def create_order():
    try:
        data = request.get_json()
        validator = OrderValidator()
        validator.validate(data)
        checking_service = Checking()
        currency_transformer = CurrencyTransformer()
        order_service = OrderService(checking_service, currency_transformer)
        result = order_service.process_order(data)
        return jsonify(success=True, data=result), 200
    except ValidationError as e:
        return jsonify(success=False, msg=str(e)), 400
    except Exception as e:
        return jsonify(success=False), 500
