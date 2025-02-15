from unittest.mock import Mock, create_autospec

from pymongo.collection import Collection

from order_system.database.menu_collection_dao import MenuCollectionDAO


def test_get_menu_when_call_succeed(test_app_context):
    with test_app_context():
        expected = {"test": "test_value"}
        mock_collection = create_autospec(Collection)
        mock_collection.find = Mock(return_value=expected)

        menu_dao = MenuCollectionDAO(mock_collection)
        assert menu_dao.get_menu_data() == expected
        mock_collection.find.assert_called_with({})


def test_get_menu_when_call_succeed_with_category(test_app_context):
    with test_app_context():
        expected = {"test": "test_value"}
        mock_collection = create_autospec(Collection)
        mock_collection.find = Mock(return_value=expected)

        menu_dao = MenuCollectionDAO(mock_collection)
        assert menu_dao.get_menu_data("entree") == expected
        mock_collection.find.assert_called_with({"category": "entree"})
