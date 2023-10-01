import schedule
import time
from datetime import datetime

import crawlWeatherDaum as weather
import crawlExchangeNaver as exchange
import kakaoMsgApi as sendKaKao
import crawlCoinMarketcap as coin
import crawlStockPriceNaver as stock

count = 0
def job():
    global count
    count = count + 1
    now = datetime.now()

    print('[메시지 보내기 작업 수행시각] {:%H:%M:%S}'.format(now))

    redirect_URI = "https://localhost:5000"

    ##날씨정보
    location = "경기도 수원시" # 날씨를 알고 싶은 지역 
    weatherMsg = weather.getWeatherDaum(location)

schedule.every(1).minutes.at(":00").do("job")   #매분 0초마다 job()수행

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
        if(count == 3) :
            schedule.clear()
            print("스케줄러 종료. 총 전송 횟수", count)
            break
    except:
        print("작업 강제 종료")
        schedule.clear()  # 기본 스케줄러 객체를 제거          
        break            # while 문을 빠져 나옴


# 작업을 위한 함수 지정
def job1():
    now = datetime.now()
    print("[작업 수행 시각] {:%H:%M:%S}".format(now))

    ##날씨정보
    location = "경기도 수원시" # 날씨를 알고 싶은 지역 
    weatherMsg = weather.getWeatherDaum(location)

    ## 환율정보
    exchangeMsg = exchange.getExchangeNaver()
    
    #코인정보
    coinMsg = coin.getCoinInfo()

    #주식정보
    stockPriceMsg = stock.getCurrentStockPrice()

    ##카카오에 메시지발송
    sendKaKao.sendKakaotalkMessage(weatherMsg)  #날씨
    sendKaKao.sendKakaotalkMessage(exchangeMsg)  #환율
    sendKaKao.sendKakaotalkMessage(coinMsg)
    sendKaKao.sendKakaotalkMessage(stockPriceMsg)


# 코드 테스트를 위해 5초마다 날씨 정보 가져와 출력하기 위한 스케줄 설정
schedule.every(5).seconds.do(job1)  # 5초(second)마다 job() 함수 실행

# -- 매일 지정한 시각에 날씨 정보를 가져와 출력하기 위한 스케줄 설정
# schedule.every().day.at("07:00").do(job) # 매일 07시에 job() 함수 실행
# schedule.every().day.at("12:00").do(job) # 매일 12시에 job() 함수 실행
# schedule.every().day.at("18:00").do(job) # 매일 18시에 job() 함수 실행

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except:
        print("작업 강제 종료")
        schedule.clear()  # 기본 스케줄러 객체를 제거          
        break            # while 문을 빠져 나옴