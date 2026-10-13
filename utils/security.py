# JWT extraction and validation logic

from fastapi import Header, HTTPException, status
from typing import Optional

def get_authenticated_customer_id(authorization: Optional[str] = Header(None)) -> str:
    """
    Extracts the user credentials or claims from the web bearer token.
    Enforces the security perimeter before passing data to the LLM agent.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Valid or active session bearer token is missing."
        )
    
    token = authorization.split(" ")[1]
    
    # PRODUCTION NOTE: Decode your JWT token here using python-jose or PyJWT
    # example: decoded_claims = jwt.decode(token, SECRET_KEY, algorithms=["RS256"])
    # customer_id = decoded_claims.get("backoffice_customer_id")
    
    mock_backoffice_customer_id = "BACKOFFICE-CUST-100123"
    return mock_backoffice_customer_id
