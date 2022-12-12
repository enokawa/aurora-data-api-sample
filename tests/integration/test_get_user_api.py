import requests
import os

import pytest

BASE_URL = os.environ["BASE_URL"]

get_user_params = [
    ("john", {"message": "hello john"}),
    ("doe", {"message": "not found"}),
]


@pytest.mark.parametrize("name, expected", get_user_params)
def test_get_user(name, expected):
    response = requests.get(f"{BASE_URL}/user/{name}")

    assert response.json() == expected
