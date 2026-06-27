from workers.WebWorker import WebWorker
from workers.YahooFinanceWorker import YahooFinanceWorkerScheduler
import json
from queue import Queue



def main():
    symbol_queue=Queue()
    currentThread=[]
    thread_count=5

    
    wikiWorker=WebWorker()
    data=[]
    with open("companies.txt","r") as f:
        data=json.load(f)

    Yahoo_Finance_Schedular_Thread=[]
    for i in range(thread_count):
        scheduler=YahooFinanceWorkerScheduler(symbol_queue)
        scheduler.start()
        Yahoo_Finance_Schedular_Thread.append(scheduler)

     
    for item in data:
        symbol=item["symbol"]
        symbol_queue.put(symbol)

    for i in range(thread_count):
        symbol_queue.put("DONE")   

    symbol_queue.join()    

    for i in range(len(Yahoo_Finance_Schedular_Thread)):
        Yahoo_Finance_Schedular_Thread[i].join()



'''
******************* OLD BATCHING APPROCH *********************

batch=[]
    for i in data:
        w2=YahooFinanceWorker(symbol=i["symbol"])
        batch.append(w2)

        if len(batch)==20:
            for worker in batch:
                worker.join()
            batch=[]    

    for worker in batch:
        worker.join()



'''

    
       

    
    

if(__name__=="__main__"):
    main()
    
