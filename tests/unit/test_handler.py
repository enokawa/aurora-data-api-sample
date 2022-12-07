import json
import pytest

from src.api.get_user import app


@pytest.fixture()
def apigw_event():
    return {
        "body": '{"test": "body"}',
        "queryStringParameters": {"foo": "bar"},
        "pathParameters": {"name": "john"},
        "httpMethod": "GET",
        "path": "/user/john",
    }


def test_fetch_user():
    ret = app.fetch_user(name="john")

    assert ret[0]["name"] == "john"


def test_handler(apigw_event):
    ret = app.handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "hello john"
