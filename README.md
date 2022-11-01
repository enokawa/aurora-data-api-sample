# aurora-data-api-sample

## Deploy the sample application

```bash
sam build
sam deploy --guided
```

## Use the SAM CLI to build and test locally

```bash
make start-api
curl http://localhost:3000/user/{id}
```

## Tests

```bash
pip install -r tests/requirements.txt --user
# unit test
python -m pytest tests/unit -v
# integration test
AWS_SAM_STACK_NAME=<stack-name> python -m pytest tests/integration -v
```
