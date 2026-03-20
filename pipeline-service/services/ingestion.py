import os
import logging

import httpx
import dlt

logger = logging.getLogger(__name__)

MOCK_SERVER_URL = os.getenv("MOCK_SERVER_URL", "http://mock-server:5000")
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@postgres:5432/customer_db"
)


def fetch_all_customers():
    """Fetch all pages from the Flask mock server."""
    all_customers = []
    page = 1
    limit = 50

    with httpx.Client(timeout=30.0) as client:
        while True:
            resp = client.get(
                f"{MOCK_SERVER_URL}/api/customers",
                params={"page": page, "limit": limit},
            )
            resp.raise_for_status()
            payload = resp.json()

            all_customers.extend(payload["data"])

            if len(all_customers) >= payload["total"] or not payload["data"]:
                break
            page += 1

    logger.info(f"Fetched {len(all_customers)} customers")
    return all_customers


@dlt.resource(
    table_name="customers", write_disposition="merge", primary_key="customer_id"
)
def customers_resource(data):
    yield from data


def run_ingestion_pipeline():
    customers = fetch_all_customers()
    if not customers:
        return 0

    pipeline = dlt.pipeline(
        pipeline_name="customer_ingestion",
        destination=dlt.destinations.postgres(credentials=DATABASE_URL),
        dataset_name="public",
    )

    pipeline.run(customers_resource(customers))
    return len(customers)
