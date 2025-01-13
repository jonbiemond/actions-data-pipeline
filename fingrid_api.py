from typing import Any

import dlt
from dlt.sources.helpers.rest_client import RESTClient
from datetime import datetime, timedelta


# wind dataset
DATASET_ID = 181


@dlt.resource(write_disposition="replace")
def resource(api_key):
    client = RESTClient(
        base_url="https://data.fingrid.fi/api/",
        headers={"x-api-key": api_key, "Accept": "application/json"},
    )
    params = {"pageSize": 1000}
    endpoint = f"datasets/{DATASET_ID}/data"
    response = client.get(endpoint, params=params)
    yield response.json()


@dlt.source
def source(api_key: str | None = dlt.secrets.value) -> Any:
    return resource(api_key)


def load() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="fingrid_api",
        destination="motherduck",
        dataset_name="fingrid_api_data",
    )
    pipeline.run(source())


if __name__ == "__main__":
    load()
