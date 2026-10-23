import asyncio
import time
from  concurrent.futures import ThreadPoolExecutor

def playing(item):
    print(f"Checking {item} is Store...")
    time.sleep(3)
    return f"{item} stocks: 50"

async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, playing, "Football")
        print(result)
    
asyncio.run(main())