from fastapi import FastAPI
app = FastAPI()

@app.get("/v1/invoices")
def get_mock_invoices(customer_id: str):
    # Simulates the JSON output TRANSACTION microservice extracts details from back office system
    return [
        {"invoice_id": "INV-2026-001", "amount": 1250.00, "status": "PAID", "due_date": "2026-11-15"},
        {"invoice_id": "INV-2026-002", "amount": 4300.50, "status": "OPEN", "due_date": "2026-12-10"}
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
