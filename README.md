# epfl-enac-deploy-action

EPFL ENAC-IT Continuous Deployment

This action makes a POST request to a given URL to deploy the app and then do a loop
to another URL until the status is `finished` or `error`
Initially created for checking if a enac deployment is complete (via enacit-ansible)

## Create two secrets in your repository

- under your repository settings in /settings/secrets/actions
- Add DEPLOYMENT_SECRET and DEPLOYMENT_ID given by the linux enacit-linux-sysadmins@epfl.ch

## Add Continuous Deployment to PROD hosting

Create `.github/workflows/deploy-prod.yml` containing :

```yml
# https://github.com/EPFL-ENAC/epfl-enac-deploy-action#readme
name: deploy-prod

"on":
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: EPFL-ENAC/epfl-enac-deploy-action@main
        with:
          ENAC_IT4R_CD_environment: "prod"
          ENAC_IT4R_CD_deployment_id: ${{ secrets.DEPLOYMENT_ID }}
          ENAC_IT4R_CD_deployment_secret: ${{ secrets.DEPLOYMENT_SECRET }}
```

## Add Continuous Deployment to TEST hosting

Create `.github/workflows/deploy-test.yml` containing :

```yml
# https://github.com/EPFL-ENAC/epfl-enac-deploy-action#readme
name: deploy-test

"on":
  push:
    branches:
      - develop

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: EPFL-ENAC/epfl-enac-deploy-action@main
        with:
          ENAC_IT4R_CD_environment: "test"
          ENAC_IT4R_CD_deployment_id: ${{ secrets.DEPLOYMENT_ID }}
          ENAC_IT4R_CD_deployment_secret: ${{ secrets.DEPLOYMENT_SECRET }}
```

## Inputs

### `ENAC_IT4R_CD_environment`

The environement to deploy to: test or prod

### `ENAC_IT4R_CD_deployment_id`

The unique id associated with the deployment

### `ENAC_IT4R_CD_deployment_secret`

- The secret associated with the deployment_id
- only viable for that unique id

### `timeout`

Timeout before giving up in seconds

### `interval`

Interval between polling in seconds

## Example usage

```
uses: EPFL-ENAC/epfl-enac-deploy-action@main
with:
  ENAC_IT4R_CD_environment: "test"
  ENAC_IT4R_CD_deployment_id: "demo-app"
  ENAC_IT4R_CD_deployment_secret: "xxx"
  timeout: 20
  interval: 5
```

## the main.sh

This script expects a json response from the polling url in the following format:

```
{
  status: "finished" | "error",
  output: "aeae",
}
```

Script exit with 1 when status is `error` and 0 when `finished`
Exit with 1 if timeout reached before receiving `error` or `finished` as status
