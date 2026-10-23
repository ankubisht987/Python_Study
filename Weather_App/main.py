from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv()

client = OpenAI(
    api_key=os.getenv("NVDIA_API_KEY"),
    base_url = "https://integrate.api.nvidia.com/v1"
)


def get_weather(city:str):
    url =f"https://wttr.in/{city.lower()}?format=%C%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"Weather in {city} is: {response.text}"
    
    return "Something Went Wrong"


def main():
    user_query = input(" > ")

    response = client.chat.completions.create(
        model= 'openrouter/free',
        messages=[
            {"role": "user", "content": user_query}
        ]
    )
    print(f"Ans-> {response.choices[0].message.content}")

# main()
print(get_weather("NOIDA"))