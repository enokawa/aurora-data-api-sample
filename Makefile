start-api:
	rm -rf .aws-sam && sam local start-api

test:
	python -m pytest tests/unit -v
