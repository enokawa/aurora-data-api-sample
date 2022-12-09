import json
import pytest
from src.api.get_user import app

fetch_user_params = [
    ("john", [{"name": "john", "email": "john@aurora-data-api-sample.dev"}]),
    ("doe", []),
]

handler_params = [
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


@pytest.mark.parametrize("name, expected", fetch_user_params)
def test_fetch_user(db_name, mocker, name, expected):
    mocker.patch("db.DATABASE", db_name)
    ret = app.fetch_user(name=name)

    assert ret == expected


@pytest.mark.parametrize("req, expected", handler_params)
def test_handler(db_name, mocker, req, expected):
    mocker.patch("db.DATABASE", db_name)
    ret = app.handler(req, "")

    assert ret == expected
