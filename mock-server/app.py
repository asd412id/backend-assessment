import json
import os

from flask import Flask, jsonify, request

app = Flask(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "customers.json")

# load customers once at startup
with open(DATA_PATH, "r") as f:
    CUSTOMERS = json.load(f)

CUSTOMERS_BY_ID = {c["customer_id"]: c for c in CUSTOMERS}


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "customers_loaded": len(CUSTOMERS)})


@app.route("/api/customers")
def get_customers():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    total = len(CUSTOMERS)
    start = (page - 1) * limit
    end = start + limit

    return jsonify(
        {
            "data": CUSTOMERS[start:end],
            "total": total,
            "page": page,
            "limit": limit,
        }
    )


@app.route("/api/customers/<customer_id>")
def get_customer(customer_id):
    customer = CUSTOMERS_BY_ID.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify({"data": customer})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
