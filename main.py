from workers.WebWorker import WebWorker
from workers.YahooFinanceWorker import YahooFinanceWorker
import json



def main():

    currentThread=[]

    w1=WebWorker()
    data=[]
    with open("companies.txt","r") as f:
        data=json.load(f)

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
       

    
    

if(__name__=="__main__"):
    main()
    
