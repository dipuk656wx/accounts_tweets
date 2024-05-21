import openpyxl
import config
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib

username = config.username
password = config.password


def send_email(sender_email, sender_password, receiver_email, messages):
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    try:
        s.login(sender_email, sender_password)
    except Exception as e:
        print("Login Failed")
        print(e)
        return

    msg = f"<b>Tweets for date: {datetime.datetime.now().strftime('%Y-%m-%d')}</b><br><br>-------------------------------------------<br><br>" + \
        "<br><br>-------------------------------------------<br><br>".join(
            messages)
    msg = msg.encode('ascii', 'ignore').decode('ascii')

    # 'html' indicates that the email body will contain HTML content
    msg_body = MIMEText(msg, 'html')

    # Create the MIMEMultipart object for the entire email
    msg_email = MIMEMultipart()
    msg_email.attach(msg_body)
    msg_email['From'] = sender_email
    msg_email['To'] = receiver_email
    msg_email['Subject'] = 'Tweets Newsletter'

    s.sendmail(sender_email, receiver_email,
               msg_email.as_string())

    # terminating the session
    s.quit()


def save_xlsx(filename, rows):
    try:
        wb = openpyxl.load_workbook(filename)
        ws = wb.worksheets[0]  # select first worksheet
    except FileNotFoundError:
        headers_row = ['date', 'time', 'tweets']
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(headers_row)
    for new_row in rows:
        ws.append(new_row)
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
    start_url = f'https://twitter.com/search?q=from%3A%40{config.account_to_be_scraped}&src=typed_query&f=live'
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


login()
first_iteration = False
while cont:
    sleep(60)
    data_list_element = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'css-1dbjc4n')))
    print(data_list_element)
    sleep(1)
    data_list_elemen = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')
    print(data_list_elemen)
    tweets = []
    i = 0
    for d in data_list_elemen:

        a = d.find_elements(By.TAG_NAME, 'a')[3]
        href_link = a.get_attribute('href')
        time_element = d.find_element(By.TAG_NAME, 'time')
        time = time_element.get_attribute('datetime')
        d = d.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')[i]
        i += 1
        txt = d.text
        if txt in ch_arr:
            continue
        ch_arr.append(txt)
        tweets.append([txt, href_link, time])

        if len(ch_arr) >= 50:
            ch_arr.pop()

    print(tweets)
    if tweets and not first_iteration:
        send_email(config.sender_email, config.sender_email_password,
                   config.reciever_email, tweets)

    first_iteration = False
    sleep(86400)
    driver.refresh()
