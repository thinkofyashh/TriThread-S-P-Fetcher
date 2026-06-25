import threading 
import requests 
from bs4 import BeautifulSoup

class WebWorker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.url="https://www.tickertape.in/stocks/collections/small-cap-stocks" # Hardcoded URL for Wiki website 
        

    @staticmethod
    def extract_sp_500_companies(page_html):
        soup=BeautifulSoup(page_html,"lxml")
        table_container=soup.find("div",id="screener-table")
        table=table_container.find("table")
        table_rows=table.find_all("tr")

        l=[]
        for row in table_rows[0:]:

            name=row.select_one("td.data-col")
            subsector=row.select_one("td.subindustry-col")
            marketcap=row.select_one("td.mrktCapf-col")

            if name and subsector and marketcap:
                number=row.find("td").get_text(strip=True)
                l.append({"number":number,"name":list(name.stripped_strings)[0],"subsector":list(subsector.stripped_strings)[0],"marketcap":list(marketcap.stripped_strings)[0]})

        return l        
        

    def get_sp_500_companies(self):
        response=requests.get(self.url)
        if response.status_code!=200:
            print("Not able to Fetch the Records .")
            return []
        else :
            return self.extract_sp_500_companies(response.text)
        

    def run(self):
        l=self.get_sp_500_companies()
        for i in l:
            print(i)

            







        
    