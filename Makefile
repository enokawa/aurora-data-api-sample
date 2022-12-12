start-api:
	sam build && sam local start-api

unit-test:
	python -m pytest tests/unit -v

integration-test:
	python -m pytest tests/integration -v

deploy:
	sam build && sam deploy

lint:
	flake8 --max-line-length=119 src/
