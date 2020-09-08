# %%
from selenium import webdriver
import chromedriver_binary
import requests
import json
import time
import schedule
import logging

# %%

json_open = open('profile.json', 'r')
json_load = json.load(json_open)

userdata = json_load["userdata"]
phone_number =  json_load["phonenumber"] 

BASE_URL = "https://api.gotinder.com/"

def main():
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

    driver = webdriver.Chrome(options=options)

    driver.get("https://tinder.com/app/recs")

    # %%
    api_key = driver.execute_script("return localStorage.getItem('TinderWeb/APIToken')")

    # api_key = null であれば、headlessじゃないwebdriverでログインさせる
    if not api_key:
        driver.quit()
        
        login(userdata)

        # driver = webdriver.Chrome(options=options)
    # %%
    


    session = requests.Session()
    headers = {
        "X-Auth-Token": api_key,
        "Content-Type": "application/json"
    }

    session.headers.update(headers)
    # %%
    count = 0 

    #一回でいいねする上限
    count_max = 100

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
            if count == count_max:
                break
        if count == count_max:
            break
    # %% 
    driver.quit()

def login(userdata):
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    options = webdriver.ChromeOptions()

    options.add_argument(
        '--user-data-dir='+ userdata
    )

    options.add_argument("--remote-debugging-port=9222") 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get("https://tinder.com/app/recs")

    # 電話番号を入力
    # phone_number =  json_load["phonenumber"] #input("電話番号を入力: ")

    phone_number = input("Enter your phone number: ")

    session = requests.session()

    # Request OTP verification code
    # url = BASE_URL + "v2/auth/sms/send?auth_type=sms"
    url = BASE_URL + "v3/auth/login?locale=ja"
    body = {
        "phone_number": phone_number
        }
    s = session.post(url, body)
    print("phone_number post :" + s.text)
    print("phone_number headers:" + s.request.headers)

    # 認証コードを入力
    url = BASE_URL + "v2/auth/login/sms"
    body = {
        "otp_code": input("認証コードを入力: "),
        "phone_number": phone_number,
        "is_update": False,
    }
    session.post(url, json=body)

# %%
# schedule.every().day.at("21:14").do(main)
main()

# while True:
#   schedule.run_pending()
#   time.sleep(60)

