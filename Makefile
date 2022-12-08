start-api:
	sam build && sam local start-api

test:
	python -m pytest tests/unit -v

deploy:
	sam build && sam deploy

lint:
	flake8 --max-line-length=119 src/
