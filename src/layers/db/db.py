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
        params['parameters'] = parameters

    response = client.execute_statement(**params)
    formated_records = json.loads(response['formattedRecords'])

    return formated_records
