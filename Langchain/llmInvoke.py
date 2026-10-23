
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent

# Load API keys from .env
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY is missing from .env")

if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY is missing from .env")

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0.7,
)

# Initialize Tavily web search
search_tool = TavilySearch(
    max_results=3,
)

tools = [search_tool]

# Create the agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are a helpful research assistant. "
        "Use the web search tool to find current information. "
        "For weather questions, search for the latest available "
        "weather information and clearly state the location."
    ),
)

# Run the agent
response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": (
                "Find the capital of India and then find "
                "its current weather."
            ),
        }
    ]
})

print("\n========================")
print("FINAL OUTPUT")
print("========================\n")

print(response["messages"][-1].content)
