from selenium import webdriver
import time
import platform
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# OS 가져오기
os_name = platform.system().lower()

options = Options()

# headless 옵션 설정
#options.add_argument('headless')
options.add_argument("no-sandbox")

# 브라우저 윈도우 사이즈
options.add_argument('window-size=2560x1440')

# 사람처럼 보이게 하는 옵션들
options.add_argument("disable-gpu")  # 가속 사용 x
options.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재
options.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정

# window일 때 소스코드 내부 chromedriver.exe 사용, mac일 때 brew에서 찾아서 씀
service = Service('chromedriver.exe' if os_name == 'windows' else '')
# 드라이버 위치 경로 입력
driver = webdriver.Chrome(service=service, options=options)

# 인천광역시 체육회
driver.get('https://www.namohagae.kro.kr/login')
driver.implicitly_wait(3)
userId = driver.find_element(By.ID, 'username')
userPassword = driver.find_element(By.ID, 'password')
form_button = driver.find_element(By.ID, 'form_button')


userId.send_keys('spring')
userPassword.send_keys('')
form_button.click()
time.sleep(300)

driver.quit()  # driver 종료
