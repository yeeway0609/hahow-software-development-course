import json

from dependency_injector.wiring import Provide, inject
from flask import current_app, request, jsonify
from flask.views import MethodView

from order_system.database.menu_collection_dao import MenuCollectionDAO
from order_system.exception import InvalidAPIUsageException


class GetMenuHandler:
    @inject
    def __init__(self, menu_collection_dao: MenuCollectionDAO):
        self.__menu_collection_dao = menu_collection_dao

    @staticmethod
    def validate_input(request_body: json):
        """確認 input 是否符合我們 API 的定義

        :param request_body:
        :return:
        """
        # 這裡應該使用 json schema 來驗證會更好，但不希望讓每個人都要花時間學 json schema，因此用最簡單的方法驗證
        allowed_fields = {"category"}
        allowed_category = {"Entree", "Side", "Drink"}
        for key in request_body.keys():
            if key not in allowed_fields:
                error_msg = "Request has unrecognized field: " + key
                current_app.logger.error(error_msg)
                raise InvalidAPIUsageException(
                    error_type="Invalid Input", message=error_msg, status_code=400
                )
            if key == "category":
                if request_body.get(key) not in allowed_category:
                    error_msg = (
                        "Request has unrecognized category value: " + request_body[key]
                    )
                    current_app.logger.error(error_msg)
                    raise InvalidAPIUsageException(
                        error_type="Invalid Input", message=error_msg, status_code=400
                    )

    def handle_request(self, request_body: json) -> dict:
        """處理 GetMenuAPI 的邏輯

        :param request_body: GetMenuInput
        :return: GetMenuOutput 符合我們 API 定義的 dict
        """
        current_app.logger.info("Received request: " + str(request_body))

        self.validate_input(request_body)

        menu = self.__menu_collection_dao.get_menu_data(
            category=request_body.get("category")
        )

        def construct_menu_item(db_menu_item: dict):
            return {
                "name": db_menu_item.get("name"),
                "category": db_menu_item.get("category"),
                "price": db_menu_item.get("price"),
            }

        response = {"menu": list(map(construct_menu_item, menu))}
        current_app.logger.info("Returning the response: " + str(response))

        return response


class GetMenuView(MethodView):
    def __init__(self, get_menu_handler: GetMenuHandler = Provide["get_menu_handler"]):
        self.__get_menu_handler = get_menu_handler

    def post(self):
        raw_response = self.__get_menu_handler.handle_request(request.json)
        return jsonify(raw_response)
