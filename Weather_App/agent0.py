# Chain Of Thought Prompting
from dotenv import load_dotenv
from openai import OpenAI
import requests
import json
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    base_url='https://openrouter.ai/api/v1'
)


def get_weather(city: str):  # CHANGED (formatting only): was `city:str`
    url = f"https://wttr.in/{city.lower()}?format=%C%t"  # CHANGED (formatting only): added space after `=`
    response = requests.get(url)

    if response.status_code == 200:
        return f"Weather in {city} is: {response.text}"

    return "Something Went Wrong"


available_tools = {  # CHANGED (formatting only): added spaces around `=`
    "get_weather": get_weather
}

# ---------------------------------------------------------------------------
# CHANGES INSIDE SYSTEM_PROMPT (not commented inside the string itself,
# because comments there would become part of the prompt sent to the model):
#
# 1. Rule line:
#    BEFORE: "The very first call will always be for the observe step which is the output from the called tool."
#    AFTER:  "After you call a tool, the next message will be an OBSERVE step which is the output from the called tool."
#
# 2. Output JSON Format line:
#    BEFORE: { "step": ..., "content": "string" ,"TOOL":"string, "input":"string"}
#    AFTER:  { "step": ..., "content": "string", "tool": "string", "input": "string" }
#    (missing quote fixed, and "TOOL" -> "tool" to match parsed_result.get("tool"))
#
# 3. Example 1, second to last PLAN line:
#    BEFORE: "Now finally lets perform the add 3.5"
#    AFTER:  "Now finally lets perform the add 2 + 1.5 = 3.5"
#
# 4. Example 2, tool call line:
#    BEFORE: PLAN: { "step": "TOOL", ... }
#    AFTER:  TOOL: { "step": "TOOL", ... }
#
# 5. Example 2, observation line:
#    BEFORE: PLAN: { "step": "OBSERVE", ... }
#    AFTER:  OBSERVE: { "step": "OBSERVE", ... }
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.

Rules:
- Strictly Follow the given JSON output format
- Only run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN (That can be multiple times), OUTPUT
- You can also call tool if required from the list of available tools.
- After you call a tool, the next message will be an OBSERVE step which is the output from the called tool.

Output JSON Format:
{ "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string" }

Available Tools:
- get_weather(city:str): Takes city name as an input string and returns the weather info about the city.

Example 1:
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: { "step": "PLAN", "content": "Seems like user is interested in math problem" }
PLAN: { "step": "PLAN", "content": "Looking at the problem, we should solve this using BODMAS" }
PLAN: { "step": "PLAN", "content": "Yes, The BODMAS is correct thing to be done here" }
PLAN: { "step": "PLAN", "content": "First we must multiply 3 * 5 which is 15" }
PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 15 / 10" }
PLAN: { "step": "PLAN", "content": "We must perform divide that is 15 / 10 = 1.5" }
PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 1.5" }
PLAN: { "step": "PLAN", "content": "Now finally lets perform the add 2 + 1.5 = 3.5" }
PLAN: { "step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as ans" }
OUTPUT: { "step": "OUTPUT", "content": "3.5" }

Example 2:
START: What is the weather of Delhi?
PLAN: { "step": "PLAN", "content": "Seems like user is interested in getting weather of Delhi." }
PLAN: { "step": "PLAN", "content": "Lets see if we have any available tool from the list of available tools" }
PLAN: { "step": "PLAN", "content": "Great, we have get_weather tool available for this query." }
PLAN: { "step": "PLAN", "content": "I need to call get_weather tool for delhi as input for city" }
TOOL: { "step": "TOOL", "tool": "get_weather", "input": "delhi" }
OBSERVE: { "step": "OBSERVE", "tool": "get_weather", "output": "The temp of delhi is cloudy with 20 C" }
PLAN: { "step": "PLAN", "content": "Great, I got the weather info about delhi" }
OUTPUT: { "step": "OUTPUT", "content": "The current weather in delhi is 20 C with some cloudy sky" }
"""

print("\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

user_query = input("👉 ")

message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model='openrouter/free',  # CHANGED (formatting only): was `model= 'openrouter/free'`
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "TOOL":
        tool_to_call = parsed_result.get("tool")  # CHANGED (formatting only): was `=parsed_result`
        tool_input = parsed_result.get("input")
        print(f"⚙️: {tool_to_call} ({tool_input})")

        tool_response = available_tools[tool_to_call](tool_input)
        print(f"⚙️: {tool_to_call} ({tool_input}) = {tool_response}")
        # CHANGED: role "developer" -> "user" (many OpenRouter models reject/ignore "developer")
        # CHANGED: "step" value "OBSERVED" -> "OBSERVE" (to match the name used in the prompt)
        message_history.append({"role": "user", "content": json.dumps(
            {"step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response}
        )})
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("🤖", parsed_result.get("content"))
        break

    # CHANGED (formatting only): indentation of this block fixed (was over-indented)
    message_history.append({
        "role": "user",
        "content": "Continue to the next step."
    })

print("\n\n\n")