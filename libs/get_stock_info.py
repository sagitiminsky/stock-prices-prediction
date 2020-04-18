from libs.Queue import Queue
import requests
from bs4 import BeautifulSoup



class GetStockInfo:
    def __init__(self,window_size,stock_names=['FB']):
        self.stocks={}
        for stock_name in stock_names:
            self.stocks[stock_name]={'link':'https://finance.yahoo.com/quote/FB?p='+stock_name,'queueObj':Queue(max_size=window_size)}


    def measure_stock(self):
        for stock_name in self.stocks:
            r=requests.get(self.stocks[stock_name]['link'])
            soup=BeautifulSoup(r.text,"lxml")
            value=float(soup.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text)
            queueObj=self.stocks[stock_name]['queueObj']
            queueObj.enqueue(value) #this step adds both value to _queue, and normalized_value to _norm_queue




