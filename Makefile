start-api:
	sam build && sam local start-api

test:
	python -m pytest tests/unit -v
