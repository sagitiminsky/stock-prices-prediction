from fastapi import FastAPI, Request, Depends, BackgroundTasks
import uvicorn
from fastapi.templating import Jinja2Templates
import apps.web_platform.models
from apps.web_platform.models import Base
from apps.web_platform.database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from apps.web_platform.models import Stock

import json
from libs.stocks.graphs.graphs import Graphs_Obj

apps.web_platform.models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")


class StockRequest(BaseModel):
    symbol: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def fetch_stock_data(id: int):
    """
    preforms a background task and updates db when done
    """
    db = SessionLocal()
    stock = db.query(Stock).filter(Stock.id == id).first()
    g = Graphs_Obj(stock.symbol)

    for time_scale in ['1m', '2m', '5m', '15m', '30m', '1h', '1d', '5d', '1mo', '3mo']:
        stock.time_scale = time_scale
        stock.open = json.dumps(g.graphs[time_scale]['open']) if 'open' in g.graphs[time_scale] else ""
        stock.low = json.dumps(g.graphs[time_scale]['low']) if 'low' in g.graphs[time_scale] else ""
        stock.high = json.dumps(g.graphs[time_scale]['high']) if 'high' in g.graphs[time_scale] else ""
        stock.close = json.dumps(g.graphs[time_scale]['close']) if 'close' in g.graphs[time_scale] else ""
        stock.volume = json.dumps(g.graphs[time_scale]['volume']) if 'volume' in g.graphs[time_scale] else ""
        stock.perceptron_model_path = ""
        db.add(stock)
        db.commit()


@app.get("/")
def home(request: Request):
    """
    displayes the dashboard / home page
    """
    return templates.TemplateResponse("home.html", {
        'request': request
    })


@app.post("/stock")
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    creates stock and stores it in the database
    """
    stock = Stock()
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()

    background_tasks.add_task(fetch_stock_data, stock.id)


@app.post("/train_model")
def train_model(request: Request):
    """
    with selected stock and time stamp and model and prediction type,
    creaetes a trained model and stores it in the cloud, in saves the path into db
    """


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
