import pytest
from flask import Flask


@pytest.fixture(scope="package")
def test_app_context():
    return Flask("test").app_context
