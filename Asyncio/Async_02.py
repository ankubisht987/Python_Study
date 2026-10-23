import asyncio
import time

async def play(items):
    print(f"We need {items} to Play....")
    # await asyncio.sleep(2)
    time.sleep(3)
    print(f"Ok you can Paly with {items}")

async def main():
    await  asyncio.gather(
        play("Football"),
        play("Cricket"),
        play("Volleyball"),
    )
asyncio.run(main())