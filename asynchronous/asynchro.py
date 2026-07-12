

import asyncio

async def make_tea():

    print("Boiling Water .....")
    await asyncio.sleep(2)
    print("Tea is Ready")

async def make_toast():
    print("Put Bread into the toast")
    await asyncio.sleep(3)
    print("Toast is ready")

result=make_tea()
print(result )

async def main():
    await asyncio.gather(
    result,
    make_toast()
)
asyncio.run(main())