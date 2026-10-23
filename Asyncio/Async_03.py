import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        print(f"Fetched {url} with status {response.status}")

async def main():
    urls = ["https://www.google.com/"] 
    async with aiohttp.ClientSession() as session:
        task = [fetch_url(session , url) for url in urls]
        await asyncio.gather(*task)
        
asyncio.run(main())