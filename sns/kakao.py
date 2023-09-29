from selenium.webdriver import Chrome
import time 
from selenium.webdriver.common.by import By
import requests
import json

# 아래의 주석을 없애고 본인의 REST API 키를 입력
REST_API_KEY = "e034f6fcdd67f07d1d948ad6826e74a3" 

# 아래의 주석을 없애고 본인의 인가 코드를 입력
CODE = "wKe_xLiHx17bFS5_oNjmGNQ49JM4MafMox4i6sdNFtuLoIpz3LwnylH1cJ89NnbPhhsrhQo9dZsAAAGK4hQqBQ"


def get_kakao_auth_code(rest_api_key, redirect_uri):
    driver = Chrome()                # 크롬 드라이버 객체 생성
    time.sleep(1)

    driver.set_window_size(800, 600) # 웹 브라우저의 창 크기 설정  

    base_url = "https://kauth.kakao.com/oauth/authorize"
    param1 = f"client_id={rest_api_key}"
    param2 = f"redirect_uri={redirect_uri}"
    param3 = "response_type=code"
    param4 = "scope=talk_message"
    
    parameters = f"{param1}&{param2}&{param3}&{param4}"
    url = base_url + "?" + parameters

    driver.get(url) # 웹 브라우저를 실행해 지정한 URL에 접속
    driver.implicitly_wait(5)
    
    # 로그인(ID 입력)
    user_email = "4simile@gmail.com"                        # 자신의 email 주소 입력
    user_id = driver.find_element(By.NAME, "email")         # name 속성으로 아이디(ID) 입력창 찾기
    # user_id = driver.find_element(By.ID, "id_email_2")    # ID 속성으로 아이디(ID) 입력창 찾기
    user_id.send_keys(user_email)                           # email 주소 입력

    # 로그인(PW 입력)
    user_password = "flowersoon123!"                        # 자신의 암호 입력
    user_pw = driver.find_element(By.NAME, "password")      # name 속성으로 패스워드(비밀번호) 입력창 찾기
    # user_pw = driver.find_element(By.ID, "id_password_3") # id 속성으로 패스워드(비밀번호) 입력창 찾기
    user_pw.send_keys(user_password)                        # 암호 입력
    time.sleep(1)

    # 로그인 버튼 클릭
    login_button = driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[8]/button[1]')
    login_button.click()
    time.sleep(3) # 다른 URL로 넘어갈 때까지 명시적으로 기다림

    redirect_url =  driver.current_url # 인가 코드가 포함된 URL을 가져옴
    auth_code = redirect_url.split("code=")[-1] # 인가 코드만 추출
    
    return auth_code


def get_kakao_access_token(rest_api_key, redirect_uri, auth_code):

    url = "https://kauth.kakao.com/oauth/token" # 카카오 메시지 API를 위한 토큰 생성 URL

    req_data = {"grant_type" : "authorization_code",
                "client_id" : rest_api_key,
                "redirect_url" : redirect_uri,
                "code" : auth_code }

    r = requests.post(url, data=req_data)
    token_info = r.json()
    
    return token_info['access_token']



def send_kakaotalk_message(access_token, text_message):
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send' # URL 생성
    headers = {"Authorization": "Bearer " + access_token}
    json_data = json.dumps({"object_type" : "text",
                          "text" : text_message,
                          "link" : {} })
    data = {"template_object": json_data} 
    r = requests.post(url, headers=headers, data=data) # POST 방법으로 요청해 응답받음

    if r.json()['result_code'] == 0:
        print('카카오톡 메시지 보내기 성공')
    else:
        print('카카오톡 메시지 보내기 실패')


sample_message = "파이썬을 이용한 카카오톡 메시지입니다."
send_kakaotalk_message(ACCESS_TOKEN, sample_message)
sample_message2 = "아래 링크를 클릭하면 해당 링크로 연결됩니다.\nwww.google.com"
send_kakaotalk_message(ACCESS_TOKEN, sample_message2)