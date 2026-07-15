


import asyncio

async def make_tea():
    print("tea is in making ")
    await asyncio.sleep(3)
    print("tea is ready")


async def make_toast():
    print("toast is in making ")
    await asyncio.sleep(3)
    print("toast is ready")    

async def main():
    await make_tea()    
    await make_toast()


asyncio.run(main())   