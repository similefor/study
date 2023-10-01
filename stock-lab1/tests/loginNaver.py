from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time

driver = Chrome()                # 크롬 드라이버 객체 생성
driver.set_window_size(800, 900) # 웹 브라우저의 창 크기 설정

url = "https://nid.naver.com/"   # 네이버 계정 로그인 URL 지정
driver.get(url)                  # 웹 브라우저를 실행해 지정한 URL에 접속

my_id = "naver_id"               # 자신의 아이디 입력
my_pw = "naver_password"         # 자신의 패스워드 입력

# 아이디 입력
script_id = f"document.getElementsByName('id')[0].value='{my_id}'"
driver.execute_script(script_id)  # 자바스크립트로 아이디 입력

# 패스워드 입력
script_pw = f"document.getElementsByName('pw')[0].value='{my_pw}'"
driver.execute_script(script_pw)  # 자바스크립트로 패스워드 입력

time.sleep(1)

# 로그인 버튼 클릭하기 
xpath = '//*[@id="log.login"]'                     # XPath
login_button = driver.find_element(By.XPATH, xpath)# XPath로 로그인 버튼 찾기
login_button.click()                               # 버튼 클릭
    
print("- 접속한 웹 사이트의 제목:", driver.title)  # 접속한 URL의 제목 출력
print("- 접속한 웹 사이트의 URL:", driver.current_url) # 접속한 URL 출력