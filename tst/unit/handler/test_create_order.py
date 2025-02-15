import json
from unittest.mock import create_autospec, Mock

import pytest

from order_system import InvalidAPIUsageException
from order_system.database.order_collection_dao import OrderCollectionDAO
from order_system.handler.create_order import CreateOrderHandler


def test_validate_input_when_succeed(test_app_context):
    with test_app_context():
        try:
            # 測試輸入符合格式的值
            CreateOrderHandler.validate_input(
                {
                    "customerName": "test_customer",
                    "orderTime": "test_time",
                    "items": ["item1", "item2"],
                }
            )
        except InvalidAPIUsageException:
            pytest.fail("Unexpected InvalidAPIUsageException ..")


def test_validate_input_when_failed(test_app_context):
    with test_app_context():
        with pytest.raises(InvalidAPIUsageException):
            # 測試輸入不存在的欄位
            CreateOrderHandler.validate_input({"bad_field": ""})
        with pytest.raises(InvalidAPIUsageException):
            # 測試輸入空值
            CreateOrderHandler.validate_input(
                {"customerName": "", "orderTime": "", "items": []}
            )
        with pytest.raises(InvalidAPIUsageException):
            # 測試輸入多餘的欄位
            CreateOrderHandler.validate_input(
                {
                    "customerName": "test_customer",
                    "orderTime": "test_time",
                    "items": ["item1"],
                    "extra": "",
                }
            )


def test_create_order_when_call_succeed(test_app_context):
    with test_app_context():
        mock_order_dao = create_autospec(OrderCollectionDAO)
        mock_order_dao.create_order_data = Mock(return_value="test_order_id")
        create_order_handler = CreateOrderHandler(mock_order_dao)

        request_body = {
            "customerName": "test_customer",
            "orderTime": "test_time",
            "items": ["item1", "item2"],
        }

        expected = {"order_id": "test_order_id"}
        assert create_order_handler.handle_request(request_body) == expected
        mock_order_dao.create_order_data.assert_called_once_with(order=request_body)
