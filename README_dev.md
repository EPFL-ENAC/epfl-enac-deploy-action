# epfl-enac-deploy-action new release setup

# setup

```bash
poetry install
```

# generate new requirements.txt

```bash
poetry export --without-hashes --format=requirements.txt --output requirements.txt
```

# test by hand

```bash
export DEPLOYMENT_SECRET=my-app-deploy-secret
poetry run python3 main.py --env test --deployment-id my-app-deploy-id
```
