import time
import sqlite3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from telegram.ext import *

import config

API_KEY = config.API_KEY

known_user = []
test = "Hi"


class User:
    def __init__(self, username, user_id, update, stud_user, stud_pw, stud_addr):
        self.username = username
        self.user_id = user_id
        self.update = update
        self.stud_user = stud_user
        self.stud_pw = stud_pw
        self.stud_addr = stud_addr


def handle_message(update, context):
    #aprint(update.message.chat)
    text = update.message.text
    print(update.message.chat.id)
    user = getUser(update.message.chat.id)
    #user = getUser(3)
    if not user:
        print("Kein Userr")
        known_user.append(User(update.message.chat.username, update.message.chat.id, "update", "", "", ""))
    else:
        print("user")
        response = check_StudIP(user.user_id)
        for res in response:
            update.message.reply_text(res)
    #update.message.reply_text("Na")
    #update.message.reply_text("Du")


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
    elif title.__contains__("Teilnehmende"):
        return "Teilnehmer"
    elif title.__contains__("Datei"):
        return "Datei"
    elif title.__contains__("Blubber"):
        return "Blubber"
    elif title.__contains__("Ankündigung"):
        return "Ankündigung"
    elif title.__contains__("Termin "):
        return "Termin"
    elif title.__contains__("Wiki "):
        return "Wiki"
    elif title.__contains__("Beiträge "):
        return "Beiträge"
    elif title.__contains__("Fragebogen "):
        return "Fragebogen"
    elif title.__contains__("Aufgaben"):
        return "Aufgabenblatt"


def getUser(searchID):
    con = sqlite3.connect('example.sqlite3')
    cur = con.cursor()
    # cur.execute("CREATE TABLE user(username text, user_id integer , user_update text, stud_user text, stud_pw text, stud_addr text)")
    # cur.execute("INSERT INTO user VALUES ('AdmiralMurtho',1086519082, '','hama7348','Test','https://elearning.hs-flensburg.de/studip/index.php?again=yes')")
    # con.commit()
    cur.execute("SELECT * FROM user WHERE user_id={}".format(searchID))
    print(cur.fetchall()[0])
    print(len(cur.fetchall()[0]))
    if len(cur.fetchall()) == 0:
        print("Kein User")
        con.close()
    else:
        print(cur.fetchall())
        user_datas = cur.fetchall()[0]
        user = User(user_datas[0], user_datas[1], user_datas[2], user_datas[3], user_datas[4], user_datas[5])
        con.close()
        return user

def changeValue(value, detail):
    pass
    # ToDo: Es muss hier noch die änderung von einer value in einem Feld verwirklciht werden

def safeUser(user):
    con = sqlite3.connect('example.sqlite3')
    cur = con.cursor()
    cur.execute(
        "INSERT INTO user VALUES (user.username,user.user_id, user.user.toString(),user.stud_user,user.stud_pw,user.stud_addr)")
    print(cur)
    con.close()


def main():
    updater = Updater(API_KEY)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling(2)


def check_StudIP(user):
    response = []
    ser = Service("/Users/haukemarquard/Documents/Python/chromedriver")
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
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
    liste = driver.find_elements(By.TAG_NAME, "tbody")
    for list in liste:
        # print(list.text)
        vorlesung = list.find_elements(By.TAG_NAME, "tr")
        for vorl in vorlesung:
            # print(vorl.text)
            icons = vorl.find_elements(By.CLASS_NAME, "hidden-small-down")
            for ic in icons:
                link = ic.find_elements(By.TAG_NAME, "img")
                for l in link:
                    title = l.get_attribute("title")
                    classes = l.get_attribute("class")
                    if classes.__contains__("icon-role-new") or classes.__contains__("icon-shape-files+new"):
                        response.append("Veranstaltung: {}, Detail: {}".format(vorl.text, detail(title)))
    time.sleep(1)
    driver.quit()
    return response


if __name__ == "__main__":
    main()
