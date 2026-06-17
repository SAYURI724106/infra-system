from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from dotenv import load_dotenv
import os
import time

load_dotenv()

email = os.getenv("INFRA_EMAIL")
password = os.getenv("INFRA_PASSWORD")

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
wait = WebDriverWait(driver, 10)

driver.get("https://enterprise.in-fra.jp/login")
time.sleep(2)

email_field = wait.until(EC.presence_of_element_located((By.ID, "name")))
email_field.send_keys(email)

password_field = driver.find_element(By.ID, "password")
password_field.send_keys(password)

login_button = driver.find_element(By.XPATH, "//button[@type='button']")
login_button.click()
time.sleep(3)

print("login ok")

driver.get("https://enterprise.in-fra.jp/scouts")
time.sleep(3)

print("scout ok")

saved_search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '保存済みの検索条件')]")))
saved_search_button.click()
time.sleep(2)

kansai_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='standard-adornment-name-1']/following::button[contains(text(), '検索')]")))
driver.execute_script("arguments[0].click();", kansai_button)
time.sleep(3)

print("kansai ok")

students = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'e12i0ovq9') and contains(@class, 'MuiBox-root')]")))
print(f"学生数: {len(students)}人")

students = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'e12i0ovq9') and contains(@class, 'MuiBox-root')]")))

# 親要素だけに絞る
student_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-1i369cv')]")
print(f"学生数: {len(student_cards)}人")

for i, card in enumerate(student_cards[:3]):
    print(f"\n--- 学生{i+1} ---")
    
    # 大学・学部
    try:
        univ = card.find_element(By.XPATH, ".//div[contains(@class, 'e12i0ovq3')]")
        print("大学:", univ.text)
    except:
        print("大学: 取得失敗")
    
    # 出勤・時間
    try:
        work_info = card.find_elements(By.XPATH, ".//p[contains(@class, 'e12i0ovq2')]//span[@class='value']")
        for w in work_info:
            print(w.text)
    except:
        print("勤務情報: 取得失敗")
        
driver.quit()
