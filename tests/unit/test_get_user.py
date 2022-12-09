import json
import pytest
from src.api.get_user import app


@pytest.fixture()
def apigw_event():
    return {
        "pathParameters": {"name": "john"},
        "path": "/user/john",
    }


apigw_event_params = [
    (
        {
            "pathParameters": {"name": "john"},
            "path": "/user/john",
        },
        {
            "statusCode": 200,
            "body": json.dumps({"message": "hello john"}),
        },
    ),
    (
        {
            "pathParameters": {"name": "doe"},
            "path": "/user/doe",
        },
        {
            "statusCode": 404,
            "body": json.dumps({"message": "not found"}),
        },
    ),
]

user_params = [
    ("john", [{"name": "john", "email": "john@aurora-data-api-sample.dev"}]),
    ("doe", []),
]


@pytest.mark.parametrize("name, expected", user_params)
def test_fetch_user(db_name, mocker, name, expected):
    mocker.patch("db.DATABASE", db_name)
    ret = app.fetch_user(name=name)

    assert ret == expected


@pytest.mark.parametrize("req, expected", apigw_event_params)
def test_handler(db_name, mocker, req, expected):
    mocker.patch("db.DATABASE", db_name)
    ret = app.handler(req, "")

    assert ret == expected
