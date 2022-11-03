import json
import os

import boto3


client = boto3.client('rds-data')
RDS_ARN = os.getenv('RDS_ARN')
SECRET_ARN = os.getenv('SECRET_ARN')
DATABASE = os.getenv('DATABASE_NAME')


def execute_select_statement(sql: str, parameters: list = None) -> list[dict]:
    params = {
        'resourceArn': RDS_ARN,
        'secretArn': SECRET_ARN,
        'sql': sql,
        'database': DATABASE,
        'formatRecordsAs': 'JSON'
    }

    if parameters:
        params['parameters'] = convert_type(parameters)

    response = client.execute_statement(**params)
    formated_records = json.loads(response['formattedRecords'])

    return formated_records


def convert_type(parameters: list) -> list[dict]:
    for parameter in parameters:
        if isinstance(parameter['value'], bool):
            parameter['value'] = {'booleanValue': parameter['value']}
        elif isinstance(parameter['value'], int):
            parameter['value'] = {'longValue': parameter['value']}
        elif isinstance(parameter['value'], float):
            parameter['value'] = {'doubleValue': parameter['value']}
        elif isinstance(parameter['value'], str):
            parameter['value'] = {'stringValue': parameter['value']}
        elif isinstance(parameter['value'], bytes):
            parameter['value'] = {'blobValue': parameter['value']}

    return parameters
