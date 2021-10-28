class Config:
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True


def logger_config(debug=False):
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://flask.logging.wsgi_errors_stream",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "./log/order_system.log",  # For convenience
                "maxBytes": 100000,
                "backupCount": 5,
            },
            "error_file": {
                "level": "ERROR",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "./log/order_system.error.log",  # For convenience
                "maxBytes": 100000,
                "backupCount": 5,
            },
        },
        "root": {
            "level": "DEBUG" if debug else "INFO",
            "handlers": ["console"] if debug else ["console", "file", "error_file"],
        },
    }
