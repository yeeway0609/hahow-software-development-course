from unittest.mock import create_autospec, Mock

from bson import ObjectId
from pymongo.collection import Collection

from order_system.database.menu_collection_dao import MenuCollectionDAO
from order_system.database.order_collection_dao import OrderCollectionDAO
from order_system.handler.get_menu import GetMenuHandler
from order_system.handler.get_order import GetOrderHandler
from order_system.handler.create_order import CreateOrderHandler


def test_get_menu_and_menu_dao_integration(test_app_context):
    with test_app_context():
        db_result = [
            {
                "name": "test_name",
                "category": "test_category",
                "price": "test_price",
            }
        ]
        mock_menu_collection = create_autospec(Collection)
        mock_menu_collection.find = Mock(return_value=db_result)
        get_menu_handler = GetMenuHandler(MenuCollectionDAO(mock_menu_collection))

        expected = {
            "menu": [
                {
                    "name": "test_name",
                    "category": "test_category",
                    "price": "test_price",
                }
            ]
        }
        assert get_menu_handler.handle_request({}) == expected


def test_get_order_and_order_dao_integration(test_app_context):
    """
    測試 GetOrderHandler 與 OrderCollectionDAO 的整合。
    模擬資料庫返回訂單數據，並檢查處理程序返回的結果是否正確。
    """
    with test_app_context():
        test_order_id = str(ObjectId())
        db_result = [
            {
                "order_id": test_order_id,
                "customerName": "test_customerName",
                "orderTime": "test_orderTime",
                "items": ["test_item1", "test_item2"],
                "total_price": 999,
                "status": "test_status",
            }
        ]
        mock_order_collection = create_autospec(Collection)
        mock_order_collection.find_one = Mock(return_value=db_result[0])
        get_order_handler = GetOrderHandler(OrderCollectionDAO(mock_order_collection))

        expected = {"order": db_result[0]}
        assert get_order_handler.handle_request({"order_id": test_order_id}) == expected


def test_create_order_and_order_dao_integration(test_app_context):
    """
    測試 CreateOrderHandler 與 OrderCollectionDAO 的整合。
    模擬資料庫插入訂單數據，並檢查處理程序返回的結果是否正確。
    """
    with test_app_context():
        test_order_id = str(ObjectId())
        mock_result = Mock(inserted_id=test_order_id)
        mock_order_collection = create_autospec(Collection)
        mock_order_collection.insert_one = Mock(return_value=mock_result)
        create_order_handler = CreateOrderHandler(
            OrderCollectionDAO(mock_order_collection)
        )

        test_request_body = {
            "customerName": "test_customer",
            "orderTime": "test_time",
            "items": ["item1", "item2"],
        }

        expected = {"order_id": test_order_id}
        assert create_order_handler.handle_request(test_request_body) == expected
