import os
import requests
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_classic import hub
from langchain_core.tools import tool
from langchain_classic.agents import create_react_agent, AgentExecutor

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")

search_tool = TavilySearchResults(max_result=3)

result = search_tool.invoke("Give me The Latest News on Football")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0.7,
)

prompt = hub.pull("hwchase17/react")

tools = [
    search_tool
]

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# ==========================================
# RUN
# ==========================================

response = agent_executor.invoke({
    "input": (
        "Find the capital of India"
        "and then find its current weather."
    )
})

print("\n========================")
print("FINAL OUTPUT")
print("========================\n")

print(response["output"])
