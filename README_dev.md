# epfl-enac-deploy-action new release setup

# setup

```bash
poetry install
```

# generate new requirements.txt

```bash
poetry export --without-hashes --format=requirements.txt --output requirements.txt
```
