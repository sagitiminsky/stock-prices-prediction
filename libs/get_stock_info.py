from libs.Queue import Queue
import requests
import bs4


class GetStockInfo:
    def __init__(self,stock_names=['FB']):
        self.stocks={}
        for stock_name in stock_names:
            self.stocks[stock_name]={'link':'https://finance.yahoo.com/quote/FB?p='+stock_name,'values':Queue()}


    def measure_stock(self):
        for stock_name in self.stocks:
            r=requests.get(self.stocks[stock_name]['link'])
            soup=bs4.BeautifulSoup(r.text,"lxml")
            self.stocks[stock_name]['values'].enqueue(float(soup.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text))
            