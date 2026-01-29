import os.path
import time
from selenium import webdriver
from datetime import datetime
import platform
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from captchaCracker.learnTest import predict_img


def get_unique_filename(directory, base_name, ext=".png"):
    counter = 0
    while True:
        suffix = "" if counter == 0 else f"_{counter}"
        path = os.path.join(directory, f"{base_name}{suffix}{ext}")
        if not os.path.exists(path):
            return path
        counter += 1

# OS 가져오기
os_name = platform.system().lower()

options = Options()
# headless 옵션 설정
options.add_argument('headless')
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
driver = webdriver.Chrome(
    executable_path='chromedriver.exe' if os_name == 'windows' else '',
    options=options
)

#  이미지 제공
driver.get('')

# 운영체제에 따라 경로 설정
if os_name == 'windows':
    save_directory = 'D:/python/captchaCracker/captchaImages'
elif os_name == 'darwin':
    home_directory = os.path.expanduser("~")
    save_directory = os.path.join(home_directory, 'python', 'captchaCracker', 'captchaImages')
else:
    raise Exception("Unsupported OS")

# 디렉터리 생성(없으면)
os.makedirs(save_directory, exist_ok=True)

#이미지 캡쳐 반복 횟수
num = 100

for i in range(num):
    temp_path = os.path.join(save_directory, "temp.png")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'img'))
        )
        img = driver.find_element(By.TAG_NAME, 'img')
        img.screenshot(temp_path)

        # 캡챠 예측
        pred_text = predict_img(
            temp_path,
            weights_path='D:/python/captchaCracker/weights/weights.h5'
        )

        # 중복 방지된 최종 파일명 생성
        final_path = get_unique_filename(save_directory, pred_text)

        os.rename(temp_path, final_path)
        print(f"Saved: {final_path}")

    except Exception as e:
        print(f"Error: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

    driver.refresh()
    time.sleep(2)

driver.quit()

