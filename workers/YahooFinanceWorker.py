import threading 
from bs4 import BeautifulSoup
import requests 

class YahooFinanceWorker(threading.Thread):
    def __init__(self,symbol,**kwargs):
        super().__init__()
        self.symbol=symbol
        base_url="https://finance.yahoo.com/quote/"
        self.url=f'{base_url}{self.symbol}'
        self.start()

    def getPrice(self):
        headers = {
    "User-Agent": "Mozilla/5.0"
}
        response=requests.get(self.url,headers=headers)
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

    def run(self):
        p=self.getPrice()
        print(p)    


