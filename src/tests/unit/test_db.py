from src.layers.db import db

def test_execute_statement():
  ret = db.execute_statement()

  assert ret == [{
    'name': 'john',
    'email': 'john@aurora-data-api-sample.dev'
  }]