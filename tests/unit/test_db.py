from src.layers.db import db


def test_execute_select_statement(mocker, testrun_uid):
    mocker.patch("db.DATABASE", testrun_uid)
    ret = db.execute_select_statement(
        sql="SELECT name, email FROM users WHERE name = :name;",
        parameters=[{"name": "name", "value": "john"}],
    )

    assert ret == [{"name": "john", "email": "john@aurora-data-api-sample.dev"}]
