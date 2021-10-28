from flask import jsonify


def invalid_api_usage_handler(error):
    """讓 flask 打包處理 error 並以 json 的形式返回

    :param error:
    :return:
    """
    response = jsonify(
        status_code=error.code if error.code else 400,
        error_type=error.name,
        description=error.description,
    )
    return response


class InvalidAPIUsageException(Exception):
    def __init__(self, error_type, message, status_code=None):
        super().__init__()
        self.name = error_type
        self.description = message
        self.code = status_code
