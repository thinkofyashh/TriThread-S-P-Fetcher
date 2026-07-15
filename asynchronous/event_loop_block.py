import asyncio 
import time


async def task_A():
    print("Boiling Water ....")
    await asyncio.sleep(3)
    print("Task A finished ")

async def main():
    task=asyncio.create_task(task_A())
    for i in range(5):
        print("Main thread Block for Sec",{i})
        time.sleep(1)


asyncio.run(main())             