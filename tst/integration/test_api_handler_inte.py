from unittest.mock import create_autospec, Mock

import pytest
from dependency_injector import containers, providers
from pymongo import MongoClient

from order_system import create_app
from order_system.database.menu_collection_dao import MenuCollectionDAO
from order_system.handler.get_menu import GetMenuHandler


class MockContainer(containers.DeclarativeContainer):
    mock_db = create_autospec(MongoClient)
    mock_order_system = Mock()
    mock_db.order_system = mock_order_system
    mock_order_system.command = Mock()

    db_client = providers.Object(mock_db)

    menu_collection_dao = providers.Callable(
        create_autospec,
        MenuCollectionDAO
    )

    get_menu_handler = providers.Factory(
        GetMenuHandler, menu_collection_dao=menu_collection_dao
    )


@pytest.fixture
def client():
    app = create_app(MockContainer())

    with app.test_client() as client:
        yield client


def test_get_menu_api(client):
    response = client.post('/get-menu/', json={})
    assert response.get_json() == {"menu": []}
