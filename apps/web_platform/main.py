from fastapi import FastAPI,Request
import uvicorn
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates=Jinja2Templates(directory="templates")
import models
from database import SessionLocal,engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home(request:Request):
    """
    displayes the dashboard / home page
    """
    return templates.TemplateResponse("home.html",{
        'request':request
    })

@app.post("/stock")
def create_stock():
    """
    creates stock and stores it in the database
    """
    return{
        'code': 'success',
        'message':'stock created'
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
