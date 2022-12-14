import json

import db


def fetch_user(name: str) -> dict:
    user = db.execute_select_statement(
        sql="SELECT name, email FROM users WHERE name = :name;",
        parameters=[{"name": "name", "value": name}],
    )

    return user


def handler(event, context):
    name = event["pathParameters"].get("name")
    user = fetch_user(name=name)
    if not user:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "not found"}),
        }

    username = user[0]["name"]

    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"hello {username}"}),
    }
