import pandas as pd
import time


# 네이버 금융의 환율 정보 웹 사이트 주소
url = 'https://finance.naver.com/marketindex/exchangeList.nhn' 

## 현재 환율정보
def getExchagneNaver():
    # url에서 표 데이터를 추출해 DataFrame 데이터의 리스트로 반환
    # 웹 사이트의 표 데이터에서 두 번째 줄을 DataFrame 데이터의 columns로 선택
    # dfs = pd.read_html(url)
    dfs = pd.read_html(url, header=1) 

    #dfs[0].head() # 전체 데이터 중 앞의 일부분만 표시

    #exchangeRateDf = dfs[0].replace({'전일대비상승': '▲', '전일대비하락': '▼'}, regex=True)

    exchangeRtDf = dfs[0].head(4)
    exchangeRtList = exchangeRtDf[['통화명','매매기준율']].values.tolist()

    exchangeRtMsg = "* 주요 통화의 환율정보 *\n"

    for exchangeRt in exchangeRtList :
        str = f"{exchangeRt[0]}:{exchangeRt[1]}원"
        exchangeRtMsg = exchangeRtMsg + str

    return exchangeRtMsg


## 과거 환율정보
# 날짜별 환율 데이터를 반환하는 함수
# - 입력 인수: currency_code(통화코드), last_page_num(페이지 수)
# - 반환: 환율 데이터
def getLastExchagneNaver(currencyCode, lastPageNum):
    baseUrl = "https://finance.naver.com/marketindex/exchangeDailyQuote.nhn"

    df = pd.DataFrame()

    for pageNum in range(1, lastPageNum+1):
        url = f"{baseUrl}?marketindexCd={currencyCode}&page={pageNum}"
        dfs = pd.read_html(url, header=1)

        if dfs[0].empty: # 통화 코드가 잘못 지정됐거나 마지막 페이지의 경우 for 문을 빠져나오기 위한 코드
            if (pageNum==1):
                print(f"통화 코드({currencyCode})가 잘못 지정됐습니다.")
            else:
                print(f"{pageNum}가 마지막 페이지입니다.")
            break

        df = pd.concat([df, dfs[0]], ignore_index=True) # page별로 가져온 DataFrame 데이터 연결
        time.sleep(0.1) # 0.1초간 멈춤
        
    return df

# ##과거환율정보 사용예
# df_usd = getLastExchagneNaver('FX_USDKRW', 2)

# df_eur = getLastExchagneNaver('FX_EURKRW', 1)

# # 행과 열의 최대 표시 개수를 임시로 설정
# with pd.option_context('display.max_rows',4, 'display.max_columns',6):
#     pd.set_option("show_dimensions", False) # 행과 열 개수 정보 숨기기
#     display(df_usd)
