from fastapi import FastAPI,Request,Depends,BackgroundTasks
import uvicorn
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates=Jinja2Templates(directory="templates")
import models
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Stock
models.Base.metadata.create_all(bind=engine)
import json
from graphs.graphs import Graphs

class StockRequest(BaseModel):
    symbol:str
    time_scale:str

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()



def fetch_stock_data(id:int):
    """
    preforms a background task and updates db when done
    """
    db=SessionLocal()
    stock = db.query(Stock).filter(Stock.id == id).first()
    g=Graphs(stock.symbol)
    stock.open=json.dumps(g.graphs[stock.time_scale]['open'])
    stock.low=json.dumps(g.graphs[stock.time_scale]['low'])
    stock.high=json.dumps(g.graphs[stock.time_scale]['high'])
    stock.close=json.dumps(g.graphs[stock.time_scale]['close'])
    stock.volume=json.dumps(g.graphs[stock.time_scale]['volume'])

    db.add(stock)
    db.commit()


@app.get("/")
def home(request:Request):
    """
    displayes the dashboard / home page
    """
    return templates.TemplateResponse("home.html",{
        'request':request
    })

@app.post("/stock")
async def create_stock(stock_request: StockRequest,background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    """
    creates stock and stores it in the database
    """
    stock=Stock()
    stock.symbol=stock_request.symbol
    stock.time_scale=stock_request.time_scale
    db.add(stock)
    db.commit()

    background_tasks.add_task(fetch_stock_data,stock.id)

@app.post("/train_model")
def train_model(request:Request):
    """
    with selected stock and time stamp and model and prediction type,
    creaetes a trained model and stores it in the cloud, in saves the path into db
    """


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
