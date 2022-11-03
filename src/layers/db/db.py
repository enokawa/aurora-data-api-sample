import json
import os

import boto3


client = boto3.client('rds-data')
RDS_ARN = os.getenv('RDS_ARN')
SECRET_ARN = os.getenv('SECRET_ARN')
DATABASE = os.getenv('DATABASE_NAME')


def execute_select_statement(sql: str, parameter_sets: list = None) -> list[dict]:
    parameters = {
        'resourceArn': RDS_ARN,
        'secretArn': SECRET_ARN,
        'sql': sql,
        'database': DATABASE,
        'formatRecordsAs': 'JSON'
    }

    if parameter_sets:
        parameters['parameterSets'] = parameter_sets

    response = client.execute_statement(**parameters)
    formated_records = json.loads(response['formattedRecords'])

    return formated_records
