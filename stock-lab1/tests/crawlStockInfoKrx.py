import requests
from bs4 import BeautifulSoup
import pandas as pd

#----------------------------------------------------
# 한국 주식의 종목 이름과 종목 코드를 가져오는 함수
#----------------------------------------------------
def getStockInfoKrx(maketType=None):
    # 한국거래소(KRX)에서 전체 상장법인 목록 가져오기
    baseUrl =  "http://kind.krx.co.kr/corpgeneral/corpList.do"
    method = "download"

    if maketType == 'kospi':
        marketType = "stockMkt"  # 주식 종목이 코스피인 경우
    elif maketType == 'kosdaq':
        marketType = "kosdaqMkt" # 주식 종목이 코스닥인 경우
    elif maketType == None:
        marketType = ""

    url = "{0}?method={1}&marketType={2}".format(baseUrl, method, marketType)

    df = pd.read_html(url, header=0)[0]
    
    # 종목코드 열을 6자리 숫자로 표시된 문자열로 변환
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}") 
    
    # 회사명과 종목코드 열 데이터만 남김
    df = df[['회사명','종목코드']]
    
    return df

# df_kospi = getStockInfoKrx('kospi')
# df_kospi.head()

# df_kosdaq = getStockInfoKrx('kosdaq')
# df_kosdaq.head()



#--------------------------------------------------
# 회사 이름을 입력하면 종목 코드를 가져오는 함수
#--------------------------------------------------
def getStockCode(company_name, maket_type=None):
    df = getStockInfoKrx(maket_type)
    code = df[df['회사명']==company_name]['종목코드'].values
    
    if(code.size !=0):
        code = code[0]    
        return code
    else:
        print(f"[Error]입력한 [{company_name}]에 대한 종목 코드가 없습니다.")


# getStockCode('삼성전자', 'kospi') # 삼성전자 주식 종목 코드 가져오기, 코스피(kospi) 지정
# getStockCode('삼성전자') # 삼성전자 주식 종목 코드 가져오기, 주식 종류는 지정 안 함
# getStockCode('현대차')
# getStockCode('현대자동차')

# companyNames = ["삼성전자", "현대자동차", "NAVER"]
# print("[현재 주식 가격(원)]")
# for companyName in companyNames:
#     stockCode = getStockCode(companyName)
#     currentStockPrice = getCurrentStockPrice(stockCode)
#     print(f"{companyName}: {currentStockPrice}")

# getStockCode('CJ 바이오사이언스', 'kosdaq') # 주식 종목 코드 가져오기, 코스닥(kosdaq) 지정
# getStockCode('CJ 바이오사이언스') # 주식 종목 코드 가져오기, 주식 종류는 지정 안 함