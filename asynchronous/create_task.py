import asyncio
import time

'''async def make_tea():
    print("Boiling the water.....")
    await asyncio.sleep(3)
    print("Tea is Ready")


async def make_toast():
    print("Kept the Bread into the Toast")
    await asyncio.sleep(4)
    print("Toast is Ready")    


async def main():
    tea=asyncio.create_task(make_tea())
    toast=asyncio.create_task(make_toast())

    print("hello whats up ")

    await tea
    


asyncio.run(main())'''


async def async_sleep():
    print("Before the Sleep")
    await asyncio.sleep(5)
    print("After the Sleep")


async def print_hello():
    print("Hello World")


async def main():
    start=time.time()
    task=asyncio.create_task(async_sleep())
    await async_sleep()
    await task
    await print_hello()
    print("total time ",time.time()-start)


asyncio.run(main())