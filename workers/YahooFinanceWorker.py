import threading 
from bs4 import BeautifulSoup
import requests 
import datetime
from decimal import Decimal


def clean_price(Price):
    if Price=="NaN":
        return None
    return Decimal(Price.replace(",",""))
    


class YahooFinanceWorkerScheduler(threading.Thread):
    def __init__(self,input_queue,output_queue):
        super().__init__()
        self.input_queue=input_queue
        self.output_queue=output_queue



    def run(self):
        while True:
            val=self.input_queue.get()
            try:
                if val=="DONE":
                  
                 break

                yahooFinanceprice=YahooFinanceWorker(val)
                price=yahooFinanceprice.getPrice()
                self.output_queue.put({
                    "symbol":val,
                    "price":clean_price(price),
                    "extracted_time":datetime.datetime.now()
                })
                #self.output_queue.put(value)
               # print(price)
            finally:
                self.input_queue.task_done()





class YahooFinanceWorker():
    def __init__(self,symbol):
        self.symbol=symbol
        base_url="https://finance.yahoo.com/quote/"
        self.url=f'{base_url}{self.symbol}'
       

    def getPrice(self):
        headers = {
    "User-Agent": "Mozilla/5.0"
}
        response=requests.get(self.url,headers=headers,timeout=10)
        if response.status_code!=200:
            print(response.status_code)
            print("Unable to Fetech the Price of the Stock .")
            return "NaN"
        page_html=response.text
        soup=BeautifulSoup(page_html,"lxml")
        price_element=soup.find("span",{'data-testid': 'qsp-price'})
        if price_element:
            price=price_element.get_text(strip=True)
            return price
        return "NaN"
    

    
          


