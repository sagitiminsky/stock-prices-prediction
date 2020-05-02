from sqlalchemy import Column,String,Integer
from database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id=Column(Integer,primary_key=True,index=True)
    symbol=Column(String,unique=True,index=True)
    opens=Column(String,unique=False,index=True)
    lows = Column(String, unique=False, index=True)
    highs = Column(String, unique=False, index=True)
    closes = Column(String, unique=False, index=True)
    volumes = Column(String, unique=False, index=True)
    perceptron_model_path=Column(String, unique=True, index=True)
