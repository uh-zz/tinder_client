from selenium import webdriver
import chromedriver_binary
import requests
import json
import time

options = webdriver.ChromeOptions()

options.add_argument(
    '--user-data-dir='
)
options.add_argument(
    '--headless'
)

options.add_argument("--remote-debugging-port=9222") 
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

driver.get("https://tinder.com/app/recs")

api_key = driver.execute_script("return localStorage.getItem('TinderWeb/APIToken')")
print("api_key:", api_key)

with requests.Session() as session:
    headers = {
        "X-Auth-Token": api_key,
        "Content-Type": "application/json"
    }

    session.headers.update(headers)

    # 女の子リスト取得
    users = session.get("https://api.gotinder.com/v2/recs/core?locale=ja")

    count = 0 
    for user in json.loads(users.text)["data"]["results"]:
        count += 1

        # 1秒待たせて手動っぽくする
        time.sleep(1)
        print("count:", count)

        user_id = user["user"]["_id"]
        print(user_id)

        # いいね!
        session.get("https://api.gotinder.com/like/{}?locale=ja".format(user_id))

        # 一回でいいねする上限
        if count == 20:
            break

driver.quit()


