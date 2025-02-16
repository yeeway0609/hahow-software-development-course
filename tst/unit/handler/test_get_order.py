import json
from unittest.mock import create_autospec, Mock

import pytest

from order_system import InvalidAPIUsageException
from order_system.database.order_collection_dao import OrderCollectionDAO
from order_system.handler.get_order import GetOrderHandler


def test_validate_input_when_succeed(test_app_context):
    with test_app_context():
        try:
            # 測試不輸入任何值
            GetOrderHandler.validate_input({})
            # 測試輸入符合格式的值
            GetOrderHandler.validate_input({"order_id": "test_order_id"})
        except InvalidAPIUsageException:
            pytest.fail("Unexpected InvalidAPIUsageException ..")


def test_validate_input_when_failed(test_app_context):
    with test_app_context():
        with pytest.raises(InvalidAPIUsageException):
            # 測試輸入不存在的欄位
            GetOrderHandler.validate_input({"bad_field": ""})
        with pytest.raises(InvalidAPIUsageException):
            # 測試輸入空值
            GetOrderHandler.validate_input({"order_id": ""})
        with pytest.raises(InvalidAPIUsageException):
            # 測試輸入多餘的欄位
            GetOrderHandler.validate_input({"order_id": "bad_order_id", "extra": ""})


def test_get_order_when_call_succeed(test_app_context):
    with test_app_context():
        db_result = [
            {
                "order_id": "test_id",
                "customerName": "test_customerName",
                "orderTime": "test_orderTime",
                "items": ["test_item1", "test_item2"],
                "total_price": 999,
                "status": "test_status",
            }
        ]
        mock_order_dao = create_autospec(OrderCollectionDAO)
        mock_order_dao.get_order_data = Mock(return_value=db_result)
        get_order_handler = GetOrderHandler(mock_order_dao)

        expected = {
            "order": [
                {
                    "order_id": "test_id",
                    "customerName": "test_customerName",
                    "orderTime": "test_orderTime",
                    "items": ["test_item1", "test_item2"],
                    "total_price": 999,
                    "status": "test_status",
                }
            ]
        }
        assert get_order_handler.handle_request({"order_id": "test_id"}) == expected
        mock_order_dao.get_order_data.assert_called_once_with(order_id="test_id")
