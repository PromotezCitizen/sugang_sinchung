from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import urllib.request
import time
import re

timeout = 60

url = "https://sugang.kumoh.ac.kr"

if __name__ == '__main__':

    # 수강신청 매크로를 위한 web browser 여는 과정
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # 제일 처음 화면에서 학부생/대학원생 구분
    #WebDriverWait(driver, timeout=timeout).until(EC.alert_is_present())
    try:Alert(driver).accept()
    except:WebDriverWait(driver,timeout=timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="WindowDiv"]')))
    driver.find_element(By.XPATH, '//*[@id="Form_link.link"]').click()

    time.sleep(3)
    # 연 웹페이지 종료
    driver.quit()