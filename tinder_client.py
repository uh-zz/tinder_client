# %%
from selenium import webdriver
import chromedriver_binary
import requests
import json
import time
import schedule
# %%
def main():
    json_open = open('profile.json', 'r')
    json_load = json.load(json_open)
    userdata = json_load["userdata"]

    # %%
    options = webdriver.ChromeOptions()

    options.add_argument(
        '--user-data-dir='+ userdata
    )
    ##このオプションをつけると画面上でブラウザを立ち上げなくて済む
    # options.add_argument(
    #     '--headless'
    # )

    options.add_argument("--remote-debugging-port=9222") 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # %%
    driver = webdriver.Chrome(options=options)

    # %%
    driver.get("https://tinder.com/app/recs")

    # %%
    BASE_URL = "https://api.gotinder.com/"
    phone_number =  json_load["phonenumber"] #input("Enter your phone number: ")
    session = requests.session()
    # Request OTP verification code
    url = BASE_URL + "v2/auth/sms/send?auth_type=sms"
    body = {"phone_number": phone_number}
    session.post(url, body )

    # %%
    api_key = driver.execute_script("return localStorage.getItem('TinderWeb/APIToken')")
    session = requests.Session()
    headers = {
        "X-Auth-Token": api_key,
        "Content-Type": "application/json"
    }

    session.headers.update(headers)
    # %%
    count = 0 

    #一回でいいねする上限
    count_mux = 100

    for n in range(6):
        # 女の子リスト取得
        users = session.get("https://api.gotinder.com/v2/recs/core?locale=ja")

        for user in json.loads(users.text)["data"]["results"]:
            count += 1

            # 0.1秒待たせて手動っぽくする
            time.sleep(0.1)

            print("count:", count)

            user_id = user["user"]["_id"]
            # print(user_id)

            # いいね!
            session.get("https://api.gotinder.com/like/{}?locale=ja".format(user_id))
            # 一回でいいねする上限
            if count == count_mux:
                break
        if count == count_mux:
            break
    # %% 
    driver.quit()

# %%
schedule.every().day.at("21:14").do(main)
  
while True:
  schedule.run_pending()
  time.sleep(60)

