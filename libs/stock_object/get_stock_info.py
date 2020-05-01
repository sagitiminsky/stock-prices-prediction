from libs.stock_object.stock_obj import StockObj
import requests
from bs4 import BeautifulSoup
import apps.ai.config


class GetStocksInfo:
    def __init__(self):
        self.stock_names= apps.ai.config.stock_names
        self.stocks={}
        for stock_name in self.stock_names:
            self.stocks[stock_name]={'link':'https://finance.yahoo.com/quote/FB?p='+stock_name,'stock_obj':StockObj(max_size=apps.ai.config.window_size,stock_name=stock_name)}


    def measure(self,mock=None):

        if mock==None:
            for stock_name in self.stocks:
                r=requests.get(self.stocks[stock_name]['link'])
                soup=BeautifulSoup(r.text,"lxml")
                value=float(soup.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text)
                queueObj=self.stocks[stock_name]['stock_obj']
                queueObj.enqueue(value) #this step adds value to _queue, normalized_value to _norm_queue and sets max and min values in queueObj

        else: #unittest
            for stock_name in self.stocks:
                queueObj = self.stocks[stock_name]['stock_obj']
                queueObj.enqueue(mock)

            return True



