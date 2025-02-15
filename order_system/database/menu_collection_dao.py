from dependency_injector.wiring import inject
from flask import current_app
from pymongo.collection import Collection
from pymongo.cursor import Cursor


class MenuCollectionDAO:
    @inject
    def __init__(self, collection: Collection):
        self.__menu_collection = collection

    def get_menu_data(self, category: str = None) -> Cursor:
        """向資料庫索取 menu 資料，若有提供 category 則只索取該 category 的 menu

        :param category:
        :return: 資料課庫中的 menu 資料
        """
        search_filter = {"category": category} if category else {}
        current_app.logger.info(
            "Start retrieving menu from mongoDB menu collection with condition: "
            + str(search_filter)
        )
        data = self.__menu_collection.find(search_filter)
        current_app.logger.info(
            "Successfully retrieved menu from mongoDB menu collection"
        )
        return data
