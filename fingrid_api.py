from typing import Any

import dlt
from dlt.common import pendulum
from dlt.common.time import ensure_pendulum_datetime
from dlt.common.typing import TAnyDateTime
from dlt.sources.helpers.rest_client import RESTClient
from datetime import datetime, timedelta


# wind dataset
DATASET_ID = 181


@dlt.source
def source(
    api_key: str | None = dlt.secrets.value,
    start_date: TAnyDateTime | None = pendulum.datetime(year=2025, month=1, day=12),
    end_date: TAnyDateTime | None = None,
) -> Any:
    start_date_ts = ensure_pendulum_datetime(start_date).int_timestamp
    end_date_ts = (
        ensure_pendulum_datetime(end_date).int_timestamp if end_date else end_date
    )

    @dlt.resource(primary_key="start_time", write_disposition="append")
    def resource(
        timestamp: dlt.sources.incremental[int] = dlt.sources.incremental(
            "startTime",
            initial_value=start_date_ts,
            end_value=end_date_ts,
            allow_external_schedulers=True,
        ),
    ):
        client = RESTClient(
            base_url="https://data.fingrid.fi/api/",
            headers={"x-api-key": api_key, "Accept": "application/json"},
        )
        start_time = timestamp.last_value
        end_time = datetime.now().isoformat()
        params = {"start_time": start_time, "end_time": end_time}
        endpoint = f"datasets/{DATASET_ID}/data"
        response = client.get(endpoint, params=params)
        yield response.json()

    return resource


def load() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="fingrid_api",
        destination="motherduck",
        dataset_name="fingrid_api_data",
    )
    pipeline.run(source())


if __name__ == "__main__":
    load()
