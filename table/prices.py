from sqlalchemy import Column,String,Integer,DateTime,Numeric
from sqlalchemy.orm import declarative_base

Base=declarative_base()



class Price(Base):

    __tablename__="prices"
    id=Column(Integer,autoincrement=True,primary_key=True)
    symbol=Column(String)
    price=Column(Numeric(10,2))
    extracted_time=Column(DateTime)

