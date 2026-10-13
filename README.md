# ai-assistant
Users ask questions in natural language and get answers from account data, transactions, invoices, statements, and FAQs

## Core Features
* **Stateless Multi-Turn Conversations:** Session context is managed purely on the client side and passed in per token request. No databases are required in the AI tier.
* **Agentic ReAct Architecture:** Employs Claude 3.5 Sonnet to dynamically evaluate user prompts, determine intent, and safely execute backend API tool chains.
* **Hardened Security Perimeter:** Decoupled architecture strictly injects authenticated Back Office Customer IDs out-of-band at the gateway layer, eliminating AI injection risks or unauthorized cross-tenant data traversal.

---

## Project Directory Structure

```text
ai-assistant/
│
├── config/
│   └── settings.py          # Environment & AWS configuration parameters
│
├── mock_services/
│   ├── mock_account.py      # Simulates Account Microservice 
│   └── mock_transaction.py  # Simulates Transaction Microservice 
│
├── services/
│   ├── bedrock_agent.py     # LangChain Agent initialisation & loop orchestration
│   └── ms_tools.py          # Microservice wrapper functions 
│
├── schemas/
│   └── chat.py              # Pydantic models for request/response serialization
│
├── utils/
│   └── security.py          # Security validation and extraction layer
│
├── .env.example             # Configuration settings template
├── docker-compose.yml       # Orchestrates the local mock network
├── Dockerfile               # High-performance multi-stage deployment build
├── main.py                  # FastAPI Application main entry point
├── README.md                # Project documentation
└── requirements.txt         # Package dependencies file
```

---

## Local Installation (Windows)

Follow these steps to set up and run the project natively on a Windows machine.

### Prerequisites
Ensure **Python 3.11** or newer is installed. Validate using:
  ```powershell
  python --version
  ```

### Step 1: Clone and Navigate to the Project
```powershell
cd /ai-assistant
```

### Step 2: Configure Environment Variables
Create a file named `.env` in the root folder based on the sample config:
```text
AWS_REGION=eu-west-2
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
ACCOUNT_SERVICE_URL=http://localhost:8001/v1/credits
TRANSACTION_SERVICE_URL=http://localhost:8002/v1/invoices
INTERNAL_API_KEY=local-dev-secret-key
```

### Step 3: Create and Activate a Python Virtual Environment
```powershell
python -m venv .venv
```
Activate the environment in **PowerShell**:
```powershell
.venv\Scripts\Activate.ps1
```
*(If you see an execution policy error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first, then rerun the activation script).*

### Step 4: Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Running the Application

### Option A: Local Native Execution (Without Docker)
To test the system locally, open three separate terminal windows with virtual environment active to run the mock infrastructure stack:

1. **Terminal 1 (Mock Account Microservice):**
   ```powershell
   python mock_services/mock_account.py
   ```
2. **Terminal 2 (Mock Transaction Microservice):**
   ```powershell
   python mock_services/mock_transaction.py
   ```
3. **Terminal 3 (Main AI Assistant Gateway):**
   ```powershell
   python main.py
   ```

### Option B: Unified Container Orchestration (With Docker Compose)
Ensure local host terminal is configured with AWS session tokens, then execute:
```powershell
docker-compose up --build
```

---

## Testing the Endpoint

Submit a test payload to the assistant simulating a customer querying their unified records via `curl`:

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
     -H "Authorization: Bearer mock-jwt-string" \
     -H "Content-Type: application/json" \
     -d '{
       "user_query": "Do I have any unpaid invoices and what is my available credit limit?",
       "chat_history": []
     }'
```

### Example Multi-Turn Stateless Payload Structure
To test follow-up context, pass previous conversation tuples inside the array:
```json
{
  "user_query": "When are they due?",
  "chat_history": [
    {"role": "human", "text": "Do I have any unpaid invoices?"},
    {"role": "ai", "text": "Yes, you have one open invoice: INV-2026-002 for £4300.50."}
  ]
}
```

---

## Production Implementation Checklists
* **Authentication:** Replace the stub inside `utils/security.py` with an actual cryptographic JWT decoder (`PyJWT`) tied to single sign-on system.
* **AWS Execution Policy:** The container host requires an IAM policy explicitly allowing `bedrock:InvokeModel` restricted to designated Claude model ARN.
* **timeouts:** Keep backend HTTP timeouts tight (max 8 to 10 seconds) within `services/ms_tools.py` to prevent cascading connection exhaustion if backend queues experience high load spikes.
