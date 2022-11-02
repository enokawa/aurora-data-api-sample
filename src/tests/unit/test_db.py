import json

import pytest

from src.layers.db import db

def test_db():
  ret = db.test()
  
  assert ret