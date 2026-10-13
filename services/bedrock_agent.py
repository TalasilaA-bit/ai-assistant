# LangChain Agent initialization and orchestration

from typing import List, Dict, Any
from langchain_aws import ChatBedrock
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from config.settings import settings
from services.ms_tools import tools_list
from schemas.chat import ChatMessage

# Initialize Bedrock with deterministic execution parameters
llm = ChatBedrock(
    model_id=settings.BEDROCK_MODEL_ID,
    region_name=settings.AWS_REGION,
    model_kwargs={"temperature": 0.0}
)

def execute_agent_loop(user_query: str, chat_history: List[ChatMessage], context: Dict[str, Any]) -> str:
    # 1. Adapt stateless payload list into native LangChain object elements
    langchain_history = []
    for msg in chat_history:
        if msg.role == "human":
            langchain_history.append(HumanMessage(content=msg.text))
        elif msg.role == "ai":
            langchain_history.append(AIMessage(content=msg.text))
            
    # 2. System prompt constraints for financial domain safety
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a highly secure, read-only operational customer service assistant. "
            "You have direct backend access to invoice records and account balances. "
            "CRITICAL: Base your response exclusively on verified facts provided by tools. "
            "If tools throw errors or time out, inform the client seamlessly without speculating."
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_tool_calling_agent(llm, tools_list, prompt)
    executor = AgentExecutor(agent=agent, tools=tools_list, max_iterations=3, verbose=True)
    
    result = executor.invoke({
        "input": user_query,
        "chat_history": langchain_history,
        "context": context
    })
    
    return result["output"]
