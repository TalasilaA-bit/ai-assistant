# FastAPI Application main entry point

from fastapi import FastAPI, Depends, HTTPException, status
from schemas.chat import ChatRequest, ChatResponse
from utils.security import get_authenticated_customer_id
from services.bedrock_agent import execute_agent_loop

app = FastAPI(title="AI Assistant Gateway")

# First Question: customer types: "What is my balance?"
# front end sends: {"user_query": "What is my balance?", "chat_history": []}
# returns "Your balance is £250."

# Second Question: customer types: "When is my next invoice due?"
# front end sends: {"user_query": "When is my next invoice due?", "chat_history": [{"role": "human", "text": "What is my balance?"},{"role": "ai", "text": "Your balance is £250."}]}
# answers the new prompt

@app.post("/api/v1/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def run_chat_session(request: ChatRequest, customer_id: str = Depends(get_authenticated_customer_id)):
    try:
        # Construct runtime tracking map
        runtime_context = {"customer_id": customer_id}
        
        # Invoke deterministic agent lifecycle execution
        agent_output = execute_agent_loop(
            user_query=request.user_query,
            chat_history=request.chat_history,
            context=runtime_context
        )
        return ChatResponse(answer=agent_output)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unhandled assistant event sequence error occurred: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
