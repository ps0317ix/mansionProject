import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import pathlib
import sqlite3
import configparser



def mappin_create_table():
    # データベースに接続する
    conn = sqlite3.connect('mappin.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE mappin(id int PRIMARY KEY, mansion_name text, pin text, created_datetime TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP,'localtime')))''')
    conn.commit()

def mappin_table_isexist():
    try:
        # データベースに接続する
        conn = sqlite3.connect('mappin.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) FROM sqlite_master 
            WHERE TYPE='table' AND name='mappin'
            """)
        if cur.fetchone()[0] == 0:
            return False
        return True
    except:
        return False

def mappin_search(cur, mansion_name):
    # try:
        # データベースに接続する
        # conn = sqlite3.connect('mappin.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        # cur = conn.cursor()
    cur.execute('SELECT * FROM mappin WHERE mansion_name = ?', (mansion_name,))
    # print(cur.fetchone()[0])
    if cur.fetchone() == None:
        return False
    return True
    # except:
    #     return False



def set_all_mappin():
    if mappin_table_isexist() == False:
        mappin_create_table()

    conn = sqlite3.connect('teikyou_hantei.db')
    cur = conn.cursor()
    contents = cur.execute('SELECT * FROM teikyou_hantei').fetchall()
    print(contents)

    # データベースに接続する
    conn = sqlite3.connect('mappin.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()

    conf = configparser.ConfigParser()
    conf.read('settings.ini')
    account_mail = conf['account']['account_mail']
    account_pass = conf['account']['account_pass']

    p = pathlib.Path('../mansionProject/chromedriver')
    print(p.cwd())
    driver = webdriver.Chrome(p)
    driver.get("https://www.google.com/maps/")

    time.sleep(3)
    element = driver.find_element_by_id('gb_70')
    element.click()

    time.sleep(3)
    element = driver.find_element_by_id('identifierId')
    element.send_keys(account_mail)
    element.send_keys(Keys.ENTER)

    time.sleep(3)
    element = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
    element.send_keys(account_pass)
    element.send_keys(Keys.ENTER)


    time.sleep(5)
    speed = 1


    for mansion in contents:
        print(mansion)
        print(mansion[1])
        if mappin_search(cur, mansion[1]) == True:
            continue
        try:
            time.sleep(3 + speed)
            element = driver.find_element_by_class_name('tactile-searchbox-input')
            print(mansion[1])
            element.send_keys(mansion[1])
            element.send_keys(Keys.ENTER)
            time.sleep(2 + speed)

            elements = driver.find_elements_by_class_name('section-action-chip-button')
            element = elements[1]
            element.click()
            time.sleep(1)

            elements = driver.find_elements_by_class_name('action-menu-has-icon')
            element = elements[3]
            element.click()
            time.sleep(1)

            element = driver.find_element_by_class_name('allxGeDnJMl__text')
            element.click()
            time.sleep(1)

            element = driver.find_element_by_class_name('section-common-input')
            print(mansion[3])
            element.send_keys(mansion[3])
            time.sleep(1)

            element = driver.find_element_by_class_name('section-dialog-footer-primary-action-button')
            element.click()
            time.sleep(1)

            element = driver.find_element_by_id('sb_cb50')
            element.click()
            time.sleep(1)

            cur.execute('INSERT INTO mappin VALUES (?, ?, ?, ?)', (mansion[0], mansion[1], "ピン植え実行済み", datetime.datetime.now()))
            conn.commit()

        except Exception as e:
            print(e)

    driver.close()


def set_mappin(transaction_id):
    if mappin_table_isexist() == False:
        mappin_create_table()

    conn = sqlite3.connect('teikyou_hantei.db')
    cur = conn.cursor()
    contents = cur.execute('SELECT * FROM teikyou_hantei WHERE transaction_id = ?', (transaction_id,)).fetchall()
    print(contents)

    # データベースに接続する
    conn = sqlite3.connect('mappin.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()

    conf = configparser.ConfigParser()
    conf.read('settings.ini')
    account_mail = conf['account']['account_mail']
    account_pass = conf['account']['account_pass']

    p = pathlib.Path('../mansionProject/chromedriver')
    print(p.cwd())
    driver = webdriver.Chrome(p)
    driver.get("https://www.google.com/maps/")

    time.sleep(3)
    element = driver.find_element_by_id('gb_70')
    element.click()

    time.sleep(3)
    element = driver.find_element_by_id('identifierId')
    element.send_keys(account_mail)
    element.send_keys(Keys.ENTER)

    time.sleep(3)
    element = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
    element.send_keys(account_pass)
    element.send_keys(Keys.ENTER)


    time.sleep(5)
    speed = 1


    for mansion in contents:
        print(mansion)
        try:
            time.sleep(3 + speed)
            element = driver.find_element_by_class_name('tactile-searchbox-input')
            print(mansion[1])
            element.send_keys(mansion[1])
            element.send_keys(Keys.ENTER)
            time.sleep(2 + speed)

            elements = driver.find_elements_by_class_name('section-action-chip-button')
            element = elements[1]
            element.click()
            time.sleep(1)

            elements = driver.find_elements_by_class_name('action-menu-has-icon')
            element = elements[3]
            element.click()
            time.sleep(1)

            element = driver.find_element_by_class_name('allxGeDnJMl__text')
            element.click()
            time.sleep(1)

            element = driver.find_element_by_class_name('section-common-input')
            print(mansion[3])
            element.send_keys(mansion[3])
            time.sleep(1)

            element = driver.find_element_by_class_name('section-dialog-footer-primary-action-button')
            element.click()
            time.sleep(1)

            element = driver.find_element_by_id('sb_cb50')
            element.click()
            time.sleep(1)

            cur.execute('INSERT INTO mappin VALUES (?, ?, ?, ?)', (mansion[0], mansion[1], "ピン植え実行済み", datetime.datetime.now()))
            conn.commit()

        except Exception as e:
            print(e)

    driver.close()