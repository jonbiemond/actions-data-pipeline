A proof-of-concept deploying a data pipeline with GitHub actions.

* Source: [Fingrid Data](https://data.fingrid.fi/en)
* Extract: [dlt](https://dlthub.com/)
* Transform & Load: [dbt](https://www.getdbt.com/)
* Warehouse: [MotherDuck](https://www.getdbt.com/)

## Prerequisites

* [Fingrid Data API key](https://data.fingrid.fi/en/instructions)
* [MotherDuck access token](https://motherduck.com/docs/key-tasks/authenticating-and-connecting-to-motherduck/authenticating-to-motherduck/#authentication-using-an-access-token)

## Deployment

The pipeline is deployed to GitHub actions.

### Extraction

The data is extracted from Fingrid using dlt.
dlt provides [step-by-step instructions](https://dlthub.com/docs/walkthroughs/deploy-a-pipeline/deploy-with-github-actions).


## Development

To run and develop the code locally, install dependencies with [`uv`](https://docs.astral.sh/uv/).
```bash
uv sync
```

### Extraction

`dlt` reads the secrets from `.dlt/secrets.toml`

```toml
# .dlt/secrets.toml
[sources]
api_key = "<api_key>"

[destination.motherduck.credentials]
database = "<db_name>"
password = "<access_token>"
```
