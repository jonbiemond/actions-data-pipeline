A proof-of-concept deploying a data pipeline with GitHub actions.

* Source: [Fingrid Data](https://data.fingrid.fi/en)
* Extract: [dlt](https://dlthub.com/)
* Transform & Load: [dbt](https://www.getdbt.com/)
* Warehouse: [MotherDuck](https://www.getdbt.com/)

## Prerequisites

* [Fingrid Data API key](https://data.fingrid.fi/en/instructions)
* [MotherDuck access token](https://motherduck.com/docs/key-tasks/authenticating-and-connecting-to-motherduck/authenticating-to-motherduck/#authentication-using-an-access-token)
* MotherDuck database

## Deployment

The pipeline is deployed to GitHub actions.
Create a fork of this repo to deploy.

### Extract

The data is extracted from Fingrid using dlt.
dlt provides [step-by-step instructions](https://dlthub.com/docs/walkthroughs/deploy-a-pipeline/deploy-with-github-actions).
Add the following secret values (typically stored in ./.dlt/secrets.toml):
- DB_NAME
- API_KEY
- MOTHERDUCK_TOKEN

in https://github.com/jonbiemond/actions-data-pipeline/settings/secrets/actions


## Development

To run and develop the code locally, install dependencies with [`uv`](https://docs.astral.sh/uv/).
```bash
uv sync
```

### Secrets

All the secrets and necessary variables are read from environment variables.
Set the following, or use a tool like [mise-en-place](https://mise.jdx.dev/).
```
API_KEY=<your_api_key>
DB_NAME=<your_db_name>
MOTHERDUCK_TOKEN=<your_motherduck_token>
```

### Extraction

`dlt` reads the secrets from `.dlt/secrets.toml`

```toml
# .dlt/secrets.toml
[sources]
api_key = "env(API_KEY)"

[destination.motherduck.credentials]
database = "env(DB_NAME)"
password = "env(MOTHERDUCK_TOKEN)"
```

### Transformation

`dbt` reads the secrets directly from environment variables.
