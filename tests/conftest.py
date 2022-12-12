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
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../src/layers/db")
)


def _convert_type(parameters: list) -> list[dict]:
    for parameter in parameters:
        if isinstance(parameter["value"], bool):
            parameter["value"] = {"booleanValue": parameter["value"]}
        elif isinstance(parameter["value"], int):
            parameter["value"] = {"longValue": parameter["value"]}
        elif isinstance(parameter["value"], float):
            parameter["value"] = {"doubleValue": parameter["value"]}
        elif isinstance(parameter["value"], str):
            parameter["value"] = {"stringValue": parameter["value"]}
        elif isinstance(parameter["value"], bytes):
            parameter["value"] = {"blobValue": parameter["value"]}

    return parameters


def execute_statement(
    sql: str, database: str = None, parameters: list = None
) -> list[dict]:
    params = {"resourceArn": RDS_ARN, "secretArn": SECRET_ARN, "sql": sql}

    if database:
        params["database"] = database

    if parameters:
        params["parameters"] = _convert_type(parameters)

    response = client.execute_statement(**params)

    return response


@pytest.fixture(scope="session", autouse=True)
def db_name():
    return "".join(choice(ascii_letters) for _ in range(10))


@pytest.fixture(scope="session", autouse=True)
def create_database(db_name):
    execute_statement(sql=f"CREATE DATABASE IF NOT EXISTS {db_name}")

    with open(SCHEMA, "r") as f:
        sqls = f.read().split(";")

    for sql in sqls[:-1]:
        execute_statement(sql=sql, database=db_name)

    yield

    execute_statement(sql=f"DROP DATABASE IF EXISTS {db_name}")


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
