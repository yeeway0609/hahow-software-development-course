import json

from dependency_injector.wiring import Provide, inject
from flask import jsonify, request
from flask.views import MethodView

from order_system.database.order_collection_dao import OrderCollectionDAO


class GetOrderHandler:
    @inject
    def __init__(self, order_collection_dao: OrderCollectionDAO):
        self.__order_collection_dao = order_collection_dao

    def handle_request(self, request_body: json):
        # 這兩行只是為了暫時讓 code 通過 pylint，以方便在課堂上進行章節６的示範
        # 同學在完成這個 function 後請將這兩行刪除
        assert self.__order_collection_dao is not None
        assert request_body is not None
        # ------------------------------

        # 完成這個 function

        raise NotImplementedError


class GetOrderView(MethodView):
    def __init__(
        self, get_order_handler: GetOrderHandler = Provide["get_order_handler"]
    ):
        self.__get_order_handler = get_order_handler

    def post(self):
        raw_response = self.__get_order_handler.handle_request(request.json)
        return jsonify(raw_response)
