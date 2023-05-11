# EPFL ENAC-IT Continuous Deployment

This action implements ENAC-IT's Continuous Deployment for your app on a given environment (test or prod).

To use it in your repository, create a workflow file named `.github/workflows/deploy-test.yml` with the following content:

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
          ENAC_IT4R_CD_deployment_id: "deployment_test_id given by ENAC-IT"
          ENAC_IT4R_CD_deployment_secret: ${{ secrets.DEPLOYMENT_TEST_SECRET }}
```

To deploy to production, name preferably that file `.github/workflows/deploy-prod.yml` and simply replace:

- `develop` with `main`
- `test` with `prod`
- `DEPLOYMENT_TEST_SECRET` with `DEPLOYMENT_PROD_SECRET`

## Create two secrets in your repository

Under your repository settings in /settings/secrets/actions

- For test: add `DEPLOYMENT_TEST_SECRET`
- For prod: add `DEPLOYMENT_PROD_SECRET`

Their values are provided by ENAC-IT while discussing the hosting agreement.

## Inputs

- `ENAC_IT4R_CD_environment`:
  The environement to deploy to: `test` or `prod` - (mandatory)

- `ENAC_IT4R_CD_deployment_id`:
  The unique id associated with the deployment - (mandatory)

- `ENAC_IT4R_CD_deployment_secret`:
  The secret associated with the deployment_id - (mandatory)

- `timeout`:
  Timeout before giving up in seconds. Default: 480 (8 minutes)

- `interval`:
  Interval between polling in seconds. Default: 2 seconds

## Example usage with custom timeout and interval

```
uses: EPFL-ENAC/epfl-enac-deploy-action@main
with:
  ENAC_IT4R_CD_environment: "test"
  ENAC_IT4R_CD_deployment_id: "my-app-deploy-id"
  ENAC_IT4R_CD_deployment_secret: ${{ secrets.DEPLOYMENT_TEST_SECRET }}
  timeout: 600
  interval: 10
```
