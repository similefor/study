from selenium.webdriver import Chrome
import time 
from selenium.webdriver.common.by import By
import requests
import json

chrome_driver = "C:\project\chromedriver-32.exe"
driver=Chrome(chrome_driver)
driver.get(UnicodeTranslateError)


# 아래의 주석을 없애고 본인의 REST API 키를 입력
REST_API_KEY = "e034f6fcdd67f07d1d948ad6826e74a3" 
REDIRECT_URI = "localhost:5000"

#CODE = "wKe_xLiHx17bFS5_oNjmGNQ49JM4MafMox4i6sdNFtuLoIpz3LwnylH1cJ89NnbPhhsrhQo9dZsAAAGK4hQqBQ"
# 1.카카오 인가코드 자동으로 얻기 :  6시간 마다 받아야함으로 웹드라이버를 이용하여 받는다.
def getKakaoAuthCode(REST_API_KEY, REDIRECT_URI = ""):
    driver = Chrome()                # 크롬 드라이버 객체 생성
    time.sleep(1)

    driver.setWindowSize(800, 600) # 웹 브라우저의 창 크기 설정  

    url = "https://kauth.kakao.com/oauth/authorize"
    param1 = f"client_id={REST_API_KEY}"
    param2 = f"redirect_uri={REDIRECT_URI}"
    param3 = "response_type=code"
    param4 = "scope=talk_message"
    
    parameters = f"{param1}&{param2}&{param3}&{param4}"
    url = url + "?" + parameters

    driver.get(url) # 웹 브라우저를 실행해 지정한 URL에 접속
    driver.implicitly_wait(5)
    
    # 로그인(ID 입력)
    userEmail = "4simile@gmail.com"                        # 자신의 email 주소 입력
    userId = driver.find_element(By.NAME, "email")         # name 속성으로 아이디(ID) 입력창 찾기
    # userId = driver.find_element(By.ID, "id_email_2")    # ID 속성으로 아이디(ID) 입력창 찾기
    userId.send_keys(userEmail)                           # email 주소 입력

    # 로그인(PW 입력)
    userPassword = "flowersoon123!"                        # 자신의 암호 입력
    userPw = driver.find_element(By.NAME, "password")      # name 속성으로 패스워드(비밀번호) 입력창 찾기
    # user_pw = driver.find_element(By.ID, "id_password_3") # id 속성으로 패스워드(비밀번호) 입력창 찾기
    userPw.send_keys(userPassword)                        # 암호 입력
    time.sleep(1)

    # 로그인 버튼 클릭
    loginButton = driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[8]/button[1]')
    loginButton.click()
    time.sleep(3) # 다른 URL로 넘어갈 때까지 명시적으로 기다림

    callbackUrl =  driver.current_url # 인가 코드가 포함된 URL을 가져옴
    authCode = callbackUrl.split("code=")[-1] # 인가 코드만 추출
    
    return authCode

# 2.액세스 토큰 얻기 : rest api 키, Redirect URI, 인가 코드로 액세스 토큰 얻기
def getKakaoAccessToken(REST_API_KEY, REDIRECT_URI, authCode):

    url = "https://kauth.kakao.com/oauth/token" # 카카오 메시지 API를 위한 토큰 생성 URL

    reqData = {"grant_type" : "authorization_code",
                "client_id" : REST_API_KEY,
                "redirect_url" : REDIRECT_URI,
                "code" : authCode }

    r = requests.post(url, data=req_data)
    tokenInfo = r.json()
    
    return tokenInfo['access_token']


# 3. 카카오톡에 메시지 보내기 : 
def sendKakaotalkMessage(txtMessage):
    
    # 인가코드얻어 액세스 토큰 얻는다. 6시간 마다 받는것이므로 매번 받을필요없이 체크할것
    authCode = getKakaoAuthCode(REST_API_KEY, REDIRECT_URI)
    accessToken = getKakaoAccessToken(REST_API_KEY, REDIRECT_URI, authCode)
    print("카카오인가코드:", authCode)
    print("카카오 액세스 토큰:", accessToken)

    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send' # URL 생성
    headers = {"Authorization": "Bearer " + accessToken}
    jsonData = json.dumps({"object_type" : "text",
                          "text" : txtMessage,
                          "link" : {} })
    data = {"template_object": jsonData} 
    r = requests.post(url, headers=headers, data=data) # POST 방법으로 요청해 응답받음

    if r.json()['result_code'] == 0:
        print('카카오톡 메시지 보내기 성공')
    else:
        print('카카오톡 메시지 보내기 실패')


#액세스 토큰으로 메시지보낸다.
# sendKakaotalkMessage("파이썬을 이용한 카카오톡 메시지입니다.")
# sendKakaotalkMessage("아래 링크를 클릭하면 해당 링크로 연결됩니다.\nwww.google.com")