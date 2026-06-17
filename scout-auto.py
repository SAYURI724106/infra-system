from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# ブラウザを起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Infraにアクセス
driver.get("https://enterprise.in-fra.jp")
time.sleep(3)

print("ログイン画面が開きました")
print("手動でログインしてください")
input("ログイン完了したらEnterを押してください...")

# ログイン後のページを確認
print("現在のURL:", driver.current_url)
print("次の処理に進みます...")

# スカウト候補一覧ページに移動
driver.get("https://enterprise.in-fra.jp/scouts")
time.sleep(3)

print("スカウト候補一覧のURL:", driver.current_url)
print("ページタイトル:", driver.title)
