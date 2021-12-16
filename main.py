# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pyperclip
from multiprocessing import Pool
from selenium import webdriver
import time
import datetime
import schedule

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib.request


def exist_element(driver, id):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True

def ticket(parameter):
    day = parameter[0]
    place = parameter[1]
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome("C:\chromedriver", options=chrome_options)
    driver.implicitly_wait(2);
    driver.get('https://www.yes24.com/Templates/FTLogin.aspx?ReturnURL=http://ticket.yes24.com/Special/41015')
    time.sleep(0.5)
    driver.set_window_position(place, 0)
    id = driver.find_element_by_css_selector("#SMemberID")
    id.click()
    pyperclip.copy("wlgn8648")
    id.send_keys(Keys.CONTROL, 'v')
    time.sleep(0.5)
    pw = driver.find_element_by_css_selector("#SMemberPassword")
    pw.click()
    pyperclip.copy("wlgn8468")
    pw.send_keys(Keys.CONTROL, 'v')
    driver.find_element_by_id("btnLogin").click()
    driver.implicitly_wait(2);

    wait = WebDriverWait(driver, 1000)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rn-bb03')))

    print(datetime.datetime.now())
    driver.find_element_by_class_name('rn-bb03').click()

    driver.switch_to.window(driver.window_handles[1])

    driver.find_element_by_id(day).click()
    if exist_element(driver, "selSeatClass"):
        Select(driver.find_element_by_id("selSeatClass")).select_by_value("1")

    driver.find_element_by_id("StepCtrlBtn01").click()
    driver.implicitly_wait(1)
    driver.execute_script("fdc_PromotionEnd()")
    time.sleep(1.5)
    driver.execute_script("fdc_DeliveryEnd()")
    time.sleep(1)
    driver.find_element_by_id("rdoPays22").click()

    Select(driver.find_element_by_id("selBank")).select_by_index(2)
    driver.find_element_by_id("cbxCancelFeeAgree").click()
    driver.find_element_by_id("chkinfoAgree").click()
    driver.execute_script("fdc_PrePayCheck()")


def pools():
    start = (time.time())
    pool = Pool(processes=2)
    pool.map(ticket, [['2022-01-15', 0], ['2022-01-16', 1000]])
    print(time.time() - start)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        date = urllib.request.urlopen('https://ticket.yes24.com').headers['Date'][5:-4]
        h, m, s = date[12:14], date[15:17], date[18:]
        print(h, m, s)
        if int(m) == 59 and int(s) >= 55:
            pools()
            break
        time.sleep(0.9)

