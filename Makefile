start-api:
	sam build && sam local start-api

test:
	python -m pytest src/tests/unit -v

deploy:
	sam build && sam deploy

lint:
	flake8 src/
