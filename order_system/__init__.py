import os

from logging.config import dictConfig

from flask import Flask

from order_system.config import logger_config, ProductionConfig, DevelopmentConfig
from order_system.exception import InvalidAPIUsageException, invalid_api_usage_handler
from order_system import handler
from order_system.containers import Container
from order_system.handler.get_menu import GetMenuView
from order_system.handler.get_order import GetOrderView
from order_system.handler.create_order import CreateOrderView

def create_app(container=Container()):
    """用來創建 flask server，同時會設定與資料庫的連結

    :param container: dependency injection framework 需要，同學無需特別鑽研
    :return: flask app
    """
    container.wire(packages=[handler])

    app = Flask(__name__)
    app.config["ENV"] = os.getenv("ENV", "development")

    if app.config["ENV"] == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    dictConfig(logger_config(debug=app.config["DEBUG"]))
    database = container.db_client()
    database.order_system.command("ping")

    app.add_url_rule("/get-menu/", view_func=GetMenuView.as_view("get-menu"))
    app.add_url_rule("/get-order", view_func=GetOrderView.as_view("get-order"))
    app.add_url_rule("/create-order", view_func=CreateOrderView.as_view("create-order"))
    app.register_error_handler(InvalidAPIUsageException, invalid_api_usage_handler)
    app.register_error_handler(500, invalid_api_usage_handler)

    return app
