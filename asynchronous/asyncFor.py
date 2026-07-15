import asyncio

async def get_numbers():
    await asyncio.sleep(1)
    yield 1
    await asyncio.sleep(1)
    yield 2 
    await asyncio.sleep(1)
    yield 3

async def main():
    async for number in get_numbers():
        print(number)


asyncio.run(main())

