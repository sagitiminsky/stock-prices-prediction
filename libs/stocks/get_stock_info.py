from libs.stocks.stock_object.stock_obj import StockObj
import requests
from bs4 import BeautifulSoup
import apps


class GetStocksInfo:
    def __init__(self, mock=None):
        self.stock_names = apps.ai.config.stock_names
        self.stocks = {}
        for stock_name in self.stock_names:
            self.stocks[stock_name] = {'link': 'https://finance.yahoo.com/quote/FB?p=' + stock_name,
                                       'stock_obj': StockObj(stock_name=stock_name, mock=mock)}

    def measure(self, mock=None):
        if mock == None:
            for stock_name in self.stocks:
                value, volume = self.get_cur_price(stock_name, mock)

                stock_object = self.stocks[stock_name]['stock_obj']
                stock_object.enqueue({'value': value, 'volume': volume})

        else:  # unittest
            for stock_name in self.stocks:
                stock_object = self.stocks[stock_name]['stock_obj']
                stock_object.enqueue(mock)

            return True

    def get_cur_price(self, stock_name, mock):
        if mock == None:
            r = requests.get(f'https://finance.yahoo.com/quote/{stock_name}?p=')
            soup = BeautifulSoup(r.text, "lxml")
            return float(
                soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text),\
                   int(soup.find_all('td', {'class': "Ta(end) Fw(600) Lh(14px)"})[6].find('span').text.replace(',', ''))

        else:
            return mock

