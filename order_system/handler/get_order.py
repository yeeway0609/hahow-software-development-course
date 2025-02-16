import json

from dependency_injector.wiring import Provide, inject
from flask import current_app, request, jsonify
from flask.views import MethodView

from order_system.database.order_collection_dao import OrderCollectionDAO
from order_system.exception import InvalidAPIUsageException


class GetOrderHandler:
    @inject
    def __init__(self, order_collection_dao: OrderCollectionDAO):
        self.__order_collection_dao = order_collection_dao

    @staticmethod
    def validate_input(request_body: json):
        """確認 input 是否符合我們 API 的定義

        :param request_body:
        :return:
        """
        allowed_fields = {"order_id"}
        for key in request_body.keys():
            # 輸入的欄位不在 allowed_fields 中
            if key not in allowed_fields:
                error_msg = "Request has unrecognized field: " + key
                current_app.logger.error(error_msg)
                raise InvalidAPIUsageException(
                    error_type="Invalid Input", message=error_msg, status_code=400
                )
            # 輸入的 id 欄位為空值
            if key == "order_id":
                if not request_body.get(key):
                    error_msg = "Request has empty id value"
                    raise InvalidAPIUsageException(
                        error_type="Invalid Input", message=error_msg, status_code=400
                    )

    def handle_request(self, request_body: json):
        """處理 GetOrderAPI 的邏輯

        :param request_body: GetOrderInput
        :return: GetOrderOutput 符合我們 API 定義的 dict
        """
        current_app.logger.info("Received request: " + str(request_body))

        self.validate_input(request_body)

        # 透過 request_body 中的 order_id 取得訂單資料
        order = self.__order_collection_dao.get_order_data(
            order_id=request_body.get("order_id")
        )

        # 因為 order_id 是唯一的，因此只會回傳一筆 dict 格式的資料
        response = {"order": order}
        current_app.logger.info("Response: " + str(response))

        return response


class GetOrderView(MethodView):
    def __init__(
        self, get_order_handler: GetOrderHandler = Provide["get_order_handler"]
    ):
        self.__get_order_handler = get_order_handler

    def post(self):
        raw_response = self.__get_order_handler.handle_request(request.json)
        return jsonify(raw_response)
