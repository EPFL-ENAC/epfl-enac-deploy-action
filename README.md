# epfl-enac-deploy-action

EPFL ENAC-IT Continuous Deployment

## Add Continuous Deployment to PROD hosting

Create `.github/workflows/deploy-prod.yml` containing :

```yml
# https://github.com/EPFL-ENAC/github-actions-runner#readme
name: deploy-prod

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: [self-hosted, deploy, prod]
    steps:
      - uses: EPFL-ENAC/epfl-enac-deploy-action@main
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```

## Add Continuous Deployment to TEST hosting

Create `.github/workflows/deploy-test.yml` containing :

```yml
# https://github.com/EPFL-ENAC/github-actions-runner#readme
name: deploy-test

on:
  push:
    branches:
      - develop

jobs:
  deploy:
    runs-on: [self-hosted, deploy, test]
    steps:
      - uses: EPFL-ENAC/epfl-enac-deploy-action@main
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```
## Add your repo to enacit packages

- https://github.com/orgs/EPFL-ENAC/packages/container/enacit-ansible/settings
