import requests
from bs4 import BeautifulSoup
import pandas as pd


#네이버 금융에서 현재주식 가격 가져오기
def getCurrentStockPrice(stockCode):
    
    baseUrl = 'https://finance.naver.com/item/main.nhn'
    url = baseUrl + "?code=" + stockCode
    
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    stockPrice = soup.select_one('p.no_today span.blind').get_text()
    
    return stockPrice

#stockCode = "005930"
#currentStockPrice = getCurrentStockPrice(stockCode)
