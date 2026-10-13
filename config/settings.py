# Environment & AWS configuration parameters

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "AI-Assistant"
    AWS_REGION: str = os.getenv("AWS_REGION", "eu-west-2")
    BEDROCK_MODEL_ID: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")
    
    # Internal Microservices Base URLs
    ACCOUNT_SERVICE_URL: str = os.getenv("ACCOUNT_SERVICE_URL", "https://atalasila.com")
    TRANSACTION_SERVICE_URL: str = os.getenv("TRANSACTION_SERVICE_URL", "https://atalasila.com")
    INTERNAL_API_KEY: str = os.getenv("INTERNAL_API_KEY", "")

settings = Settings()
