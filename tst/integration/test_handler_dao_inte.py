from unittest.mock import create_autospec, Mock

from pymongo.collection import Collection

from order_system.database.menu_collection_dao import MenuCollectionDAO
from order_system.handler.get_menu import GetMenuHandler


def test_get_menu_and_menu_dao_integration(test_app_context):
    with test_app_context():
        db_result = [{
            "name": "test_name",
            "category": "test_category",
            "price": "test_price",
        }]
        mock_menu_collection = create_autospec(Collection)
        mock_menu_collection.find = Mock(return_value=db_result)
        get_menu_handler = GetMenuHandler(MenuCollectionDAO(mock_menu_collection))

        expected = {
            "menu": [{
                "name": "test_name",
                "category": "test_category",
                "price": "test_price",
            }]
        }
        assert get_menu_handler.handle_request({}) == expected
