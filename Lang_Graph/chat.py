from typing_extensions import TypeDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph

class State(TypeDict):
    message:Annotated(list, add_messages)
    
graph_builder= StateGraph(state)