import time

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models.customer import Customer
from services.ingestion import run_ingestion_pipeline

app = FastAPI(title="Customer Data Pipeline")


@app.on_event("startup")
def startup():
    # give postgres time to start
    time.sleep(2)


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.post("/api/ingest")
def ingest_data():
    """Fetch all data from Flask and load into PostgreSQL."""
    try:
        count = run_ingestion_pipeline()
        return {"status": "success", "records_processed": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/customers")
def get_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.query(Customer).count()
    offset = (page - 1) * limit
    customers = (
        db.query(Customer)
        .order_by(Customer.customer_id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "data": [c.to_dict() for c in customers],
        "total": total,
        "page": page,
        "limit": limit,
    }


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"data": customer.to_dict()}
