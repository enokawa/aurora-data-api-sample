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
make test
```
