# Customer Data Pipeline

Data pipeline with 3 Docker services: Flask mock API → FastAPI ingestion (dlt) → PostgreSQL.

## How to Run

```bash
docker-compose up -d --build
```

## Testing

```bash
# health check
curl http://localhost:5000/api/health

# get customers from flask (paginated)
curl "http://localhost:5000/api/customers?page=1&limit=5"

# single customer
curl http://localhost:5000/api/customers/CUST-001

# ingest data into postgres
curl -X POST http://localhost:8000/api/ingest

# get customers from postgres
curl "http://localhost:8000/api/customers?page=1&limit=5"

# single customer from postgres
curl http://localhost:8000/api/customers/CUST-001
```

## Services

- **mock-server** (port 5000) - Flask API serving customer data from JSON file
- **pipeline-service** (port 8000) - FastAPI + dlt pipeline, ingests into PostgreSQL
- **postgres** (port 5432) - PostgreSQL 15 database

## Cleanup

```bash
docker-compose down -v
```
