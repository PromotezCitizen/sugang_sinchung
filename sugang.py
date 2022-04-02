from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # chrome web driver를 따로 설치할 필요 없이 실행 시 다운로드

import urllib.request # 서버 시간을 얻어오기 위해 사용
import time # time.sleep
import re # 
import os
import shutil

url = "https://sugang.kumoh.ac.kr/html/index.html" # 수강신청 최초 사이트
min = '00'; sec = '00' # 수강신청 열리는 시간(분, 초)
timeout = 60 # 웹페이지 로딩 최대 대기시간 : 60초
sugang_list = [] # 과목코드 추가용

if __name__ == '__main__':
    # 변수에 값 대입
    id = input("학번을 입력해주세요 >> ")
    pw = input("비밀번호를 입력해주세요 >> ")
    while True:
        code = input("과목코드를 입력해주세요(입력 종료는 exit 입니다) >> ")
        if (code == "exit"):
            break
        elif (code == ""):
            continue
        sugang_list.append(code)
    print("\n수강 리스트는\n[{}]\n입니다.\n".format(']\n['.join(sugang_list)))

    # 수강신청 매크로를 위한 web browser 여는 과정
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # 제일 처음 화면에서 학부생/대학원생 구분
    WebDriverWait(driver,timeout=timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Page00"]')))
    driver.find_element(By.XPATH, '//*[@id="Form_link.link"]').click()

    # 학부생용 수강신청 로그인 페이지 진입. 아이디, 비밀번호 입력
    WebDriverWait(driver,timeout=timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Form_버튼.pb_확인"]')))
    driver.find_element(By.XPATH, '//*[@id="Form_로그인.아이디"]').send_keys(id)
    driver.find_element(By.XPATH, '//*[@id="Form_로그인.비밀번호"]').send_keys(pw)

    # 서버시간이 00분00초가 될 떄따지 대기
    # server_time : [min, sec]으로 구분. 문자열으로 저장
    while True:
        server_time = re.split("[:]+", urllib.request.urlopen(driver.current_url).headers['Date'][-9:-4])
        print(f"Server time - {server_time[0]}min {server_time[1]}sec")
        if (server_time[0] == min):
            if (server_time[1] == sec):
                break
        time.sleep(0.3)

    # 서버시간이 10:00이 되었더라도 로그인 실패 가능성이 있음(핑 차이 등으로 59:59.90이 될 수도 있다)
    # 이를 막기 위해 0.1초마다 로그인 버튼 클릭하도록 설정
    login = driver.find_element(By.XPATH, '//*[@id="Form_버튼.pb_확인"]')
    while True:
        login.click()
        try:
            Alert(driver).accept()
        except:
            break
        time.sleep(0.1)

    # 수강신청 페이지로 이동하였다면
    # 위의 sugang_list에 등록된 과목코드를 자동으로 입력 및 수강신청
    WebDriverWait(driver,timeout=timeout).until(EC.presence_of_element_located(By.XPATH, '//*[@id="Form_버튼.pb1"]'))
    for sugangcode in sugang_list:
        driver.find_element(By.XPATH, '//*[@id="Form_희망수강과목입력.개설교과목코드"]').clear()
        driver.find_element(By.XPATH, '//*[@id="Form_희망수강과목입력.개설교과목코드"]').send_keys(sugangcode)
        driver.find_element(By.XPATH, '//*[@id="Form_버튼.pb1"]').click()
        try:
            Alert(driver).accept()
            Alert(driver).accept()
            Alert(driver).accept()
        except:
            time.sleep(0.3)
            continue
    
    # 수강신청이 끝났다면 닫기 버튼을 통해 세션 종료
    driver.find_element(By.XPATH, '//*[@id="Form2.pb1"]').click()

    # 연 웹페이지 종료 및 다운로드한 webdriver 삭제
    driver.quit()
    shutil.rmtree(os.path.join(os.path.expanduser("~"), ".wdm"))