import asyncio

async def task_A():
    print("Boiling Water .....")
    await asyncio.sleep(4)
    raise ValueError(" Task A is Failed .")

async def task_B():
    print("Bread is Put inside the Toast maker .")
    for i in range(10):
        await asyncio.sleep(1)
        print("Task B is still running in the BG .")
    print("Task B is Finally Done")

# With Task Group

async def handle_with_taskGroup():
    try :
        async with asyncio.TaskGroup() as tg:
            tg.create_task(task_A()) 
            tg.create_task(task_B())
    except* ValueError as eg:
        for e in eg.exceptions:
            print(e)               

async def main():
    try :
        handle=asyncio.create_task(handle_with_taskGroup())
        await asyncio.sleep(7)
    except Exception as e :
        print(e)   

asyncio.run(main())


