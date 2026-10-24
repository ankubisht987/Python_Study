from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from typing import Optional , Literal
import os

load_dotenv()

gemeni = init_chat_model(
    "google_genai:gemini-3.8-flash"
)

openrouter = init_chat_model(
    "openai:openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

class State(TypedDict):
    user_query: list
    llm_response: Optional[list]
    is_good :Optional[bool]
    model_used: Optional[str]
    
def chatbot(state:State):
    try:
        response = gemeni.invoke(state["user_query"])

        return {
            "llm_response": response.content,
            "is_good": True,
            "model_used": "Gemini"
        }
    except Exception as e:
        return {
            "llm_response": str(e),
            "is_good": False,
            "model_used": None
        }

def evaluate_state(state:State) -> Literal["chatbot_Openrouter", "endnode"]:
    
    if state["is_good"] and state["llm_response"]:
        return "endnode"
    
    return "chatbot_Openrouter"

def chatbot_Openrouter(state:State):
    try:
        response = openrouter.invoke(state["user_query"])

        return {
            "llm_response": response.content,
            "is_good": True,
            "model_used": "OpenRouter"
        }
    except Exception as e:
        return {
            "llm_response": str(e),
            "is_good": False,
            "model_used": None
        }

def endnode(state:State):
    return state

graph_builder= StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_Openrouter", chatbot_Openrouter)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START ,"chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_state)

graph_builder.add_edge("chatbot_Openrouter", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

query = graph.invoke({
    "user_query": "What is 20 + 20?",
    "llm_response": None,
    "is_good": None
})

print("Graph built successfully!")
print(f"Final response from {query.get('model_used', 'Unknown model')}:", query["llm_response"])
print("Primary model succeeded:", query["is_good"])