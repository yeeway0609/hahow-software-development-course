import os

from dependency_injector import containers, providers
from pymongo import MongoClient

from order_system.database.menu_collection_dao import MenuCollectionDAO
from order_system.database.order_collection_dao import OrderCollectionDAO
from order_system.handler.create_order import CreateOrderHandler
from order_system.handler.get_menu import GetMenuHandler
from order_system.handler.get_order import GetOrderHandler


class Container(containers.DeclarativeContainer):
    db_client = providers.Singleton(
        MongoClient,
        host=os.getenv("MONGO_ENDPOINT"),
    )

    menu_collection_dao = providers.Singleton(
        MenuCollectionDAO, collection=db_client.provided.order_system.menu
    )
    order_collection_dao = providers.Singleton(
        OrderCollectionDAO, collection=db_client.provided.order_system.order
    )

    get_menu_handler = providers.Factory(
        GetMenuHandler, menu_collection_dao=menu_collection_dao
    )

    get_order_handler = providers.Factory(
        GetOrderHandler, order_collection_dao=order_collection_dao
    )

    create_order_handler = providers.Factory(
        CreateOrderHandler, order_collection_dao=order_collection_dao
    )
