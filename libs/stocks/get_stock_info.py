from libs.stocks.stock_object.stock_obj import StockObj
import requests
from bs4 import BeautifulSoup
import apps
import yfinance as yf


class GetStocksInfo:
    def __init__(self,mock=None):
        self.stock_names= apps.ai.config.stock_names
        self.stocks={}
        for stock_name in self.stock_names:
            self.stocks[stock_name]={'link':'https://finance.yahoo.com/quote/FB?p='+stock_name,'stock_obj':StockObj(stock_name=stock_name,mock=mock)}

    def measure(self,mock=None):

        if mock==None:
            for stock_name in self.stocks:
                r=requests.get(self.stocks[stock_name]['link'])
                soup=BeautifulSoup(r.text,"lxml")
                value=float(soup.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text)
                volume=yf.Ticker(stock_name).get_info()['volume']
                stock_object=self.stocks[stock_name]['stock_obj']
                stock_object.enqueue({'value':value,'volume':volume})

        else: #unittest
            for stock_name in self.stocks:
                stock_object = self.stocks[stock_name]['stock_obj']
                stock_object.enqueue(mock)

            return True


