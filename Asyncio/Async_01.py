import asyncio

async def play():
    print("Playing Games..........")
    await asyncio.sleep(2)
    print("We take Break Now we play again")

asyncio.run(play())