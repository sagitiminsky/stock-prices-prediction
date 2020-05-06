from sqlalchemy import Column,String,Integer,ARRAY,FLOAT,BLOB
from apps.web_platform.database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer,primary_key=True,index=True)
    symbol = Column(String,unique=False,index=True)
    open = Column(String,unique=False,index=True)
    low = Column(String, unique=False, index=True)
    high = Column(String, unique=False, index=True)
    close = Column(String, unique=False, index=True)
    volume = Column(String, unique=False, index=True)
    time_scale = Column(String, unique=False, index=True)
    perceptron_model_path=Column(String, unique=False, index=True)
