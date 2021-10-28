import json
from unittest.mock import create_autospec, Mock

import pytest

from order_system import InvalidAPIUsageException
from order_system.database.menu_collection_dao import MenuCollectionDAO
from order_system.handler.get_menu import GetMenuHandler


def test_validate_input_when_succeed(test_app_context):
    with test_app_context():
        try:
            GetMenuHandler.validate_input({})
            GetMenuHandler.validate_input({"category": "Entree"})
            GetMenuHandler.validate_input({"category": "Side"})
            GetMenuHandler.validate_input({"category": "Drink"})
        except InvalidAPIUsageException:
            pytest.fail("Unexpected InvalidAPIUsageException ..")


def test_validate_input_when_failed(test_app_context):
    with test_app_context():
        with pytest.raises(InvalidAPIUsageException):
            GetMenuHandler.validate_input({"bad_field": ""})
        with pytest.raises(InvalidAPIUsageException):
            GetMenuHandler.validate_input({"category": "bad_cat"})
        with pytest.raises(InvalidAPIUsageException):
            GetMenuHandler.validate_input({"category": "Entree", "extra": ""})


def test_get_menu_when_call_succeed(test_app_context):
    with test_app_context():
        db_result = [{
            "name": "test_name",
            "category": "test_category",
            "price": "test_price",
        }]
        mock_menu_dao = create_autospec(MenuCollectionDAO)
        mock_menu_dao.get_menu_data = Mock(return_value=db_result)
        get_menu_handler = GetMenuHandler(mock_menu_dao)

        expected = {
            "menu": [{
                "name": "test_name",
                "category": "test_category",
                "price": "test_price",
            }]
        }
        assert get_menu_handler.handle_request({}) == expected
        mock_menu_dao.get_menu_data.assert_called_once_with(category=None)


def test_get_menu_when_call_succeed_with_category(test_app_context):
    with test_app_context():
        db_result = [{
            "name": "test_name",
            "category": "test_category",
            "price": "test_price",
        }]
        mock_menu_dao = create_autospec(MenuCollectionDAO)
        mock_menu_dao.get_menu_data = Mock(return_value=db_result)
        get_menu_handler = GetMenuHandler(mock_menu_dao)

        expected = {
            "menu": [{
                "name": "test_name",
                "category": "test_category",
                "price": "test_price",
            }]
        }
        assert get_menu_handler.handle_request({"category": "Entree"}) == expected
        mock_menu_dao.get_menu_data.assert_called_once_with(category="Entree")


def test_get_menu_when_call_succeed_with_missing_db_field(test_app_context):
    with test_app_context():
        db_result = [{
            "name": "test_name",
            "category": "test_category",
        }]
        mock_menu_dao = create_autospec(MenuCollectionDAO)
        mock_menu_dao.get_menu_data = Mock(return_value=db_result)
        get_menu = GetMenuHandler(mock_menu_dao)

        expected = {
            "menu": [{
                "name": "test_name",
                "category": "test_category",
                "price": None,
            }]
        }
        assert get_menu.handle_request({}) == expected
        mock_menu_dao.get_menu_data.assert_called_with(category=None)
