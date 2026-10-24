from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    "google_genai:gemini-3.8-flash"
)

class State(TypedDict):
    message:Annotated[list, add_messages]
    
def chatbot(state:State):
    response  = llm.invoke(state.get("message"))
    return {"message":[response]}

def secondChat(state:State):
    print("We are inside secondChat Node: " , State)
    return {"message":"Hi This is the message from secondChat Node"}

graph_builder= StateGraph(State)

graph_builder.add_node("chatbot" ,chatbot)
graph_builder.add_node("secondChat" ,secondChat)

graph_builder.add_edge(START , "chatbot")
graph_builder.add_edge("chatbot" , "secondChat")
graph_builder.add_edge("secondChat" , END)

graph = graph_builder.compile()

update_state = graph.invoke(State({"message": ["Hi, My Name is Ankush Bisht"]}))
print("\n\n update_state",update_state)