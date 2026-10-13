# Microservice wrapper functions

import requests
from typing import Dict, Any
from langchain_core.tools import tool
from config.settings import settings

@tool(parse_docstring=True)
def get_credit_balance(context: Dict[str, Any]) -> str:
    """Retrieve the current available credit balance and limit for the customer."""
    cust_id = context.get("customer_id")
    try:
        response = requests.get(
            f"{settings.ACCOUNT_SERVICE_URL}/{cust_id}", 
            headers={"X-Internal-Secret": settings.INTERNAL_API_KEY},
            timeout=8.0
        )
        if response.status_code == 200:
            return str(response.json())
        return f"Error: Backend returned HTTP status {response.status_code}."
    except requests.exceptions.Timeout:
        return "Error: Request to the internal credit microservice timed out."
    except Exception as e:
        return f"Internal system failure: {str(e)}"

@tool(parse_docstring=True)
def get_invoices(context: Dict[str, Any]) -> str:
    """Fetch past invoice tracking records, payment status flags, and balances for the consumer."""
    cust_id = context.get("customer_id")
    try:
        response = requests.get(
            f"{settings.TRANSACTION_SERVICE_URL}?customer_id={cust_id}",
            headers={"X-Internal-Secret": settings.INTERNAL_API_KEY},
            timeout=8.0
        )
        if response.status_code == 200:
            # Enforce data pruning to optimize context window tokens
            return str(response.json()[:10]) 
        return f"Error: Backend returned HTTP status {response.status_code}."
    except requests.exceptions.Timeout:
        return "Error: Request to the internal invoice microservice timed out."
    except Exception as e:
        return f"Internal system failure: {str(e)}"

tools_list = [get_credit_balance, get_invoices]
