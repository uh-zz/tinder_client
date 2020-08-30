from selenium import webdriver
import chromedriver_binary
import requests

options = webdriver.ChromeOptions()

options.add_argument(
    '--user-data-dir=/Users/uh-zz/Library/Application Support/Google/Chrome/'
)
options.add_argument(
    '--headless'
)

options.add_argument("--remote-debugging-port=9222") 
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)

driver.get("https://tinder.com/app/recs")

session = requests.session()

for cookie in driver.get_cookies():
    session.cookies.set(cookie['name'], cookie['value'])
    print(cookie['name'], cookie['value'])

result = session.get("https://api.gotinder.com/v2/recs/core?locale=ja")

print(result.text)

# ユーザ取得
# users = driver.get("https://api.gotinder.com/v2/recs/core?locale=ja")
# print(users)

# postする場所
# "https://api.gotinder.com/like/{_id}?locale=ja"

driver.quit()


