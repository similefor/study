from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import requests
import pandas as pd


def getCoinInfo(page_num):
    driver = Chrome() # 크롬 드라이버 객체 생성
    
    # page 추가해 URL 지정
    url = f"https://coinmarketcap.com/ko/?page={page_num}"
    driver.get(url)  # 웹 브라우저를 실행해 지정한 URL에 접속

    # 웹 사이트 문서 높이 가져오기
    scrollHeight = driver.execute_script("return document.body.scrollHeight")

    y = 0           # Y축 좌표의 초깃값
    yStep = 1000   # Y축 아래로 이동하는 단계
    while (True):
        y = y + yStep
        script =  "window.scrollTo(0,{0})".format(y)
        driver.execute_script(script) # 스크립트 실행
        driver.implicitly_wait(5) # 스크롤 수행 후 데이터를 받아올 때까지 기다림

        # 수식 스크롤 위치가 문서 끝보다 크거나 같으면 while 문 빠져나가기
        if (y >= scrollHeight):
            break

    html = driver.page_source # HTML 코드를 가져옴
    dfs = pd.read_html(html)  # HTML 소스에서 table의 내용을 DataFrame 리스트로 변환

    df = dfs[0] # 리스트의 첫 번째 요소를 선택
    
    # '이름' 열의 내용 변경
    df['이름'] = [name.replace(str(num), " ") for num, name in zip(df['#'], df['이름'])]
    df['이름'] = [name.replace("구매하기", "") for name in df['이름']]
    
    driver.quit() # 웹 브라우저를 종료함

    dfCoin = df.iloc[:,1:9]
    dfCoinSel = dfCoin.iloc[0:5,1:3]
    coinInfoList = dfCoinSel.values.tolist()

    coinInfoMsg = "*주요 가상 화폐 가격 정보*"
    
    for coinInfo in coinInfoList :
        str = f"> {coinInfo[0]}: {coinInfo[1]}"
        coinInfoMsg = coinInfoMsg + "\n" + str

    print(coinInfoMsg)
    return coinInfoMsg


def getCoinInfoBase(page_num):
    driver = Chrome() # 크롬 드라이버 객체 생성
    
    # page 추가해 URL 지정
    url = f"https://coinmarketcap.com/ko/?page={page_num}"
    driver.get(url)  # 웹 브라우저를 실행해 지정한 URL에 접속

    # 웹 사이트 문서 높이 가져오기
    scrollHeight = driver.execute_script("return document.body.scrollHeight")

    y = 0           # Y축 좌표의 초깃값
    yStep = 1000   # Y축 아래로 이동하는 단계
    while (True):
        y = y + yStep
        script =  "window.scrollTo(0,{0})".format(y)
        driver.execute_script(script) # 스크립트 실행
        driver.implicitly_wait(5) # 스크롤 수행 후 데이터를 받아올 때까지 기다림

        # 수식 스크롤 위치가 문서 끝보다 크거나 같으면 while 문 빠져나가기
        if (y >= scrollHeight):
            break

    html = driver.page_source # HTML 코드를 가져옴
    dfs = pd.read_html(html)  # HTML 소스에서 table의 내용을 DataFrame 리스트로 변환

    df = dfs[0] # 리스트의 첫 번째 요소를 선택
    
    # '이름' 열의 내용 변경
    df['이름'] = [name.replace(str(num), " ") for num, name in zip(df['#'], df['이름'])]
    df['이름'] = [name.replace("구매하기", "") for name in df['이름']]
    
    driver.quit() # 웹 브라우저를 종료함

    return df.iloc[:,1:9]


# pageNum = 1 # page 지정
# dfCoin = getCoinInfoBase(pageNum) # 함수 호출

#dfCoin.iloc[0:5,1:3]   #원하는 행(0~4)과 열(1~2)을 선택해 출력

# # DataFrame 데이터에서 행과 열을 선택해 출력
# with pd.option_context('display.max_rows',6):
#     pd.set_option("show_dimensions", False) # DataFrame의 행과 열 개수 출력 안 하기
#     display(dfCoin.iloc[:,0:6])