import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from telegram.ext import *

import config

API_KEY = config.API_KEY


def handle_message(update, context):
    text = update.message.text
    # response = create_response(text)
    response = check_StudIP()
    for res in response:
        update.message.reply_text(res)

def create_response(input_text):
    if input_text == 'hi':
        return "Hey Ho!"
    else:
        return "Das habe ich leider nicht verstanden"


def detail(title):
    if title.__contains__("Evaluation"):
        return "Evaluation"
    elif title.__contains__("Meeting"):
        return "Meeting"


def main():
    updater = Updater(API_KEY)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling(2)
    # check_StudIP()


def check_StudIP():
    response = []
    ser = Service("/Users/haukemarquard/Documents/Python/chromedriver")
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    driver.get("https://elearning.hs-flensburg.de/studip/index.php?again=yes")
    print(driver.title)
    ''' Login '''
    login = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, "loginname"))
    # login = driver.find_element(By.ID, "loginname")
    login.send_keys(config.username)
    pw = driver.find_element(By.ID, "password")
    pw.send_keys(config.pw)
    pw.send_keys(Keys.ENTER)
    time.sleep(2)
    ''' wechsel zu Veranstaltungen '''
    veranst = driver.find_element(By.ID, "nav_browse")
    veranst.click()

    ''' Liste an Veranstaltungen '''
    liste = driver.find_element(By.TAG_NAME, "tbody")
    # print(liste.text)
    vorlesung = liste.find_elements(By.TAG_NAME, "tr")
    for vorl in vorlesung:
        # print(vorl.text)
        icons = vorl.find_elements(By.CLASS_NAME, "hidden-small-down")
        for ic in icons:
            link = ic.find_elements(By.TAG_NAME, "img")
            for l in link:
                title = l.get_attribute("title")
                classes = l.get_attribute("class")
                if classes.__contains__("icon-role-new"):
                    response.append("Veranstaltung: {}, Detail: {}".format(vorl.text, detail(title)))
    time.sleep(1)
    driver.quit()
    return response

if __name__ == "__main__":
    main()