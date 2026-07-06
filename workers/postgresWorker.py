import threading 
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table.prices import Price
from dotenv import load_dotenv

load_dotenv()
class PostgresWorkerSchedular(threading.Thread):
    def __init__(self,input_queue):
        super().__init__()
        self.input_queue=input_queue


    def run(self):
        while True:
            val=self.input_queue.get()
            try :
                if val =="DONE":
                    break

                worker=PostgresWorker(
                    symbol=val["symbol"],
                    price=val["price"],
                    extracted_time=val["extracted_time"]
                )
                try:
                    worker.insert_into_db()
                except Exception as e:
                    print(f"Failed to insert the record for the {val['symbol']} : {e} in the DB .")    
            finally:
                self.input_queue.task_done()    


class PostgresWorker:
    def __init__(self,symbol,price,extracted_time):
        self.symbol=symbol
        self.price=price
        self.extracted_time=extracted_time
        self.db=os.environ.get("DATABASE_URL") or ""
        self.engine=create_engine(self.db)
        self.Session=sessionmaker(bind=self.engine)

    def insert_into_db(self):

        with self.Session() as session:
            price_record=Price(
                symbol=self.symbol,
                price=self.price,
                extracted_time=self.extracted_time
            )

            session.add(price_record)
            session.commit()





        
