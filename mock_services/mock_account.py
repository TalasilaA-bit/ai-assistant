from fastapi import FastAPI
app = FastAPI()

@app.get("/v1/credits/{customer_id}")
def get_mock_credit(customer_id: str):
    # Simulates what back office system would return synchronously for the customer
    return {
        "backoffice_customer_id": customer_id,
        "credit_limit": 50000.00,
        "available_credit": 34250.00,
        "currency": "GBP",
        "backoffice_source_system": "SRC_PRD"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
