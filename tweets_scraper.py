import openpyxl
import config

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.common.keys import Keys


username = config.username
password = config.password
def write_list_to_excel(filename, data):
    try:
        wb = openpyxl.load_workbook(filename)
        ws = wb.worksheets[0]  # select first worksheet
    except FileNotFoundError:
        headers_row = ["tweet_text", "userId", "date_time", "img_src", "reply", "retweet", "like"]
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(headers_row)
    for d in data:
        ws.append(d)
    wb.save(filename)



# options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(service=Service(
#     executable_path='./chromedriver'), options=options)
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 50)
ch_arr = []


cont = True


def login():
    start_url = f'https://twitter.com/search?q=abc&src=recent_search_click&f=live'
    driver.get(start_url)
    try:
        user_input_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//input[@autocomplete="username"]')))
    except:
        return False
    user_input_field.send_keys(username)
    sleep(1)
    next_btns = driver.find_elements(By.XPATH, '//div[@role="button"]')
    try:

        next_btn = next_btns[2]
    except:
        return False
    next_btn.click()
    try:

        user_password_field = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="current-password"]')))
    except:
        return False
    user_password_field.send_keys(password)
    try:
        submit_btns = driver.find_elements(By.XPATH, '//div[@role="button"]')
    except:
        return False
    submit_btn = submit_btns[2]
    submit_btn.click()



def twitter(keywords):
    for keyword in keywords:
        print(keyword)
        try:
            search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]')))
        except:
            print('Try again')
            continue
        search_input.click()
        try:
            clear_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="clearButton"]')))
        except:
            print("Try again")
            continue
        clear_btn.click()
        search_input.clear()
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.RETURN)
        while True:
            sleep(15)
            data_list_element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'css-1dbjc4n')))
            sleep(2)
            data_list_elemen = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')
            tweets_texts = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
            replies = driver.find_elements(By.XPATH, '//div[@data-testid="reply"]')
            retweets = driver.find_elements(By.XPATH, '//div[@data-testid="retweet"]')
            likes = driver.find_elements(By.XPATH, '//div[@data-testid="like"]')
            tweets = []
            i = 0
            for i, d in enumerate(data_list_elemen):
                try:
                    tweet_text = tweets_texts[i].text.strip()
                except:
                    tweet_text = ""
                try:
                    userId = d.find_element(By.XPATH, './div/div/article/div/div/div[@class="css-1dbjc4n r-18u37iz"]/div[@class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]/div/div/div/div/div/div[@class="css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t"]/div/div')
                    userId = userId.text.strip()
                except:
                    userId = ""
                try:
                    time = d.find_element(By.XPATH,'./div/div/article/div/div/div[@class="css-1dbjc4n r-18u37iz"]/div[@class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]/div/div/div/div/div/div[@class="css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t"]/div/div[@class="css-1dbjc4n r-18u37iz r-1q142lx"]/a/time')
                    date_time = time.get_attribute("datetime")
                except:
                    try:
                        time = d.find_element(By.XPATH,'./div/div/article/div/div/div[@class="css-1dbjc4n r-18u37iz"]/div[@class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]/div/div/div/div/div/div[@class="css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t"]/div/div[@class="css-1dbjc4n r-18u37iz r-1q142lx"]/div/a/time')
                        date_time = time.get_attribute("datetime")
                    except:
                        date_time =""
                try:
                    img = d.find_element(By.XPATH, './div/div/article/div/div/div[@class="css-1dbjc4n r-18u37iz"]/div[@class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]/div[@class="css-1dbjc4n r-1ssbvtb r-1s2bzr4"]/div/div/div/div/div/div/a/div/div[@class="r-1p0dtai r-1pi2tsx r-1d2f490 r-u8s1d r-ipm5af r-13qz1uu"]/div/img')
                    img_src = img.get_attribute('src')
                except:
                    img_src = ""
                try:
                    reply = replies[i].text.strip() if replies[i].text.strip() else 0
                    retweet = retweets[i].text.strip() if retweets[i].text.strip() else 0
                    like = likes[i].text.strip() if likes[i].text.strip() else 0

                except:
                    reply=0
                    retweet = 0
                    like = 0
                data = [tweet_text, userId, date_time, img_src, reply, retweet, like]
                tweets.append(data)
            write_list_to_excel(f'{keyword}.xlsx', tweets)
            break
def main():
    login()
    keywords = input("Enter the keywords separated by ,: ").split('//')
    while True:
        twitter(keywords)
        sleep(15)
main()



