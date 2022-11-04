import json

import db


def fetch_user(name: str) -> dict:
    user = db.execute_select_statement(
        sql='''SELECT `name`, `email` FROM `users`
        WHERE `name` = :name;''',
        parameters=[{'name': 'name', 'value': name}]
    )

    return user


def handler(event, context):
    print(event)
    user = fetch_user(name='john')
    name = user[0]['name']
    print(f'user: {user}')
    print(f'name: {name}')
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'hello {name}'
        }),
    }
