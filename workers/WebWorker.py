import threading 
import requests 
from bs4 import BeautifulSoup
import json



class WebWorker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.url="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies" # Hardcoded URL for Wiki website 
        

    @staticmethod
    def extract_sp_500_companies(page_html):
        soup=BeautifulSoup(page_html,"lxml")
        table_container=soup.find("table",id="constituents")
        if table_container is None:
            return []
       # table=table_container.find("table")
        table_rows=table_container.find_all("tr")[1:]

        l=[]
        for number,row in enumerate(table_rows[0:],start=1):
            row_elements=row.find_all("td")

            if len(row_elements)>=2:
                symbol=row_elements[0].get_text(strip=True)
                name=row_elements[1].get_text(strip=True)
                l.append({"number":number,"symbol":symbol,"name":name})

        return l        
    def get_sp_500_companies(self):
        headers={
            "User-Agent":"Mozilla/5.0 (compatible; SP500Scraper/1.0)"
        }
        response=requests.get(self.url,headers=headers,timeout=10)
        if response.status_code!=200:
            print(f"Not able to Fetch the Records. Status code: {response.status_code}")
            return []
        else :
            return self.extract_sp_500_companies(response.text)
        

    def run(self):
        l=self.get_sp_500_companies()
        with open("companies.txt","w") as f:
            json.dump(l,f,indent=2)
            


            







        
    
