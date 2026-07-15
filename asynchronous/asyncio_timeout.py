import asyncio


async def make_tea():
    print("Boiling water ....")
    await asyncio.sleep(4)
    print("Tea is ready ")


async def make_toast():
    print("Put Bread into the Toast Machine....")
    await asyncio.sleep(4)
    print("Toast is ready ") 



async def main():
    try :

        tea=asyncio.create_task(make_tea())
        toast=asyncio.create_task(make_toast())
        done,pending=await asyncio.wait({tea,toast},timeout=5)
        print("Done",len(done)," ","Pending :",len(pending))
        
        
    except asyncio.TimeoutError:
        print("Encountereed Timeout Error .")

asyncio.run(main())

    
     


    
