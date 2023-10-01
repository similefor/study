import requests  
from bs4 import BeautifulSoup 
import time

def getWeatherDaum(location):
    
    #location = "경기도 수원시" # 날씨를 알고 싶은 지역 
    searchQuery = location + " 날씨"
    searchUrl = "https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q="

    url = searchUrl + searchQuery
    htmlWeather = requests.get(url).text
    time.sleep(2)    
    soupWeather = BeautifulSoup(htmlWeather, "lxml")
    
    txtTemp = soupWeather.select_one('strong.txt_temp').get_text()
    txtWeather = soupWeather.select_one('span.txt_weather').get_text()

    dlWeatherDds = soupWeather.select('dl.dl_weather dd')
    [windSpeed, humidity, pm10] = [x.get_text() for x in dlWeatherDds]

    weatherInfo1 = f"- 설정지역 : {location}\n"
    weatherInfo2 = f"- 기온 : {txtTemp}\n"
    weatherInfo3 = f"- 날씨 정보 : {txtWeather}\n"
    weatherInfo4 = f"- 현재 풍속 : {windSpeed}\n"
    weatherInfo5 = f"- 현재 습도 : {humidity}\n"
    weatherInfo6 = f"- 미세 먼지 : {pm10}\n"

    weatherMsg = "[오늘의 날씨 정보]\n" + weatherInfo1 + weatherInfo2 + weatherInfo3 + \
        weatherInfo4 + weatherInfo5 + weatherInfo6

    print(weatherMsg)
    
    return weatherMsg