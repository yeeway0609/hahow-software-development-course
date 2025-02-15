import json

from dependency_injector.wiring import Provide, inject
from flask import current_app, request, jsonify
from flask.views import MethodView

from order_system.database.order_collection_dao import OrderCollectionDAO
from order_system.exception import InvalidAPIUsageException


class CreateOrderHandler:
    @inject
    def __init__(self, order_collection_dao: OrderCollectionDAO):
        self.__order_collection_dao = order_collection_dao

    @staticmethod
    def validate_input(request_body: json):
        """確認 input 是否符合我們 API 的定義

        :param request_body:
        :return:
        """
        allowed_fields = {"customerName", "orderTime", "items"}
        for key in request_body.keys():
            # 輸入的欄位不在 allowed_fields 中
            if key not in allowed_fields:
                error_msg = "Request has unrecognized field: " + key
                current_app.logger.error(error_msg)
                raise InvalidAPIUsageException(
                    error_type="Invalid Input", message=error_msg, status_code=400
                )
            # 輸入的 customerName, orderTime, items 欄位為空值
            if key in {"customerName", "orderTime", "items"}:
                if not request_body.get(key):
                    error_msg = f"Request has empty {key} value"
                    raise InvalidAPIUsageException(
                        error_type="Invalid Input", message=error_msg, status_code=400
                    )

    def handle_request(self, request_body: json):
        """處理 CreateOrderAPI 的邏輯

        :param request_body: CreateOrderInput
        :return: CreateOrderOutput 符合我們 API 定義的 dict
        """
        current_app.logger.info("Received request: " + str(request_body))

        self.validate_input(request_body)

        order_id = self.__order_collection_dao.create_order_data(order=request_body)

        response = {"order_id": str(order_id)}
        current_app.logger.info("Successfully created order: " + str(response))

        return response


class CreateOrderView(MethodView):
    def __init__(
        self, create_order_handler: CreateOrderHandler = Provide["create_order_handler"]
    ):
        self.__create_order_handler = create_order_handler

    def post(self):
        raw_response = self.__create_order_handler.handle_request(request.json)
        return jsonify(raw_response)
