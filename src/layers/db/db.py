import json
import os

import boto3


client = boto3.client('rds-data')
RDS_ARN = os.getenv('RDS_ARN')
SECRET_ARN = os.getenv('SECRET_ARN')
DATABASE = os.getenv('DATABASE_NAME')


def execute_statement() -> list[dict]:
  response = client.execute_statement(
    resourceArn=RDS_ARN,
    secretArn=SECRET_ARN,
    sql='SELECT `name`, `email` FROM `users`;',
    database=DATABASE,
    includeResultMetadata=True,
    formatRecordsAs='JSON'
  )
  
  formated = response['formattedRecords']

  return json.loads(formated)