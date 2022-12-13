import sys
import os

import pytest
import boto3
from random import choice
from string import ascii_letters

client = boto3.client("rds-data")
RDS_ARN = os.getenv("RDS_ARN")
SECRET_ARN = os.getenv("SECRET_ARN")
SCHEMA = "sql/00_schema.sql"
DATA = "sql/01_data.sql"
TABLES = ["users"]

sys.path.append(
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../../src/layers/db")
)


def execute_statement(
    sql: str, database: str = None, parameters: list = None
) -> list[dict]:
    params = {"resourceArn": RDS_ARN, "secretArn": SECRET_ARN, "sql": sql}

    if database:
        params["database"] = database
    if parameters:
        params["parameters"] = parameters

    return client.execute_statement(**params)


@pytest.fixture(scope="session", autouse=True)
def db_name():
    prefix = "test_"
    letters = "".join(choice(ascii_letters) for _ in range(10))

    return prefix + letters


@pytest.fixture(scope="session", autouse=True)
def create_schema(db_name):
    execute_statement(sql=f"CREATE DATABASE IF NOT EXISTS {db_name}")

    with open(SCHEMA, "r") as f:
        sqls = f.read().split(";")

    for sql in sqls[:-1]:
        execute_statement(sql=sql, database=db_name)

    yield

    execute_statement(sql=f"DROP DATABASE IF EXISTS {db_name}")


@pytest.fixture(scope="function", autouse=True)
def mock_db_name(mocker, db_name):
    mocker.patch("db.DATABASE", db_name)


@pytest.fixture(scope="session", autouse=True)
def insert_data(db_name):
    with open(DATA, "r") as f:
        sqls = f.read().split(";")

    for sql in sqls[:-1]:
        execute_statement(sql=sql, database=db_name)


@pytest.fixture(scope="function", autouse=False)
def truncate(db_name):
    def _truncate(table: str):
        execute_statement(sql=f"TRUNCATE TABLE {table}", database=db_name)

    return _truncate


@pytest.fixture(scope="function", autouse=False)
def truncate_all(truncate):
    for table in TABLES:
        truncate(table)
