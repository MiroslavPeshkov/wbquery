import requests
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import re
import datetime
import streamlit as st
import numpy as np
from shutil import which
import os, sys
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe


firefoxOptions = Options()
FIREFOXPATH = which("firefox")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
firefoxOptions.add_argument(f'user-agent={user_agent}')
firefoxOptions.add_argument('--headless')
firefoxOptions.add_argument('--no-sandbox')
firefoxOptions.add_argument("--window-size=1920,1080")
firefoxOptions.add_argument('--disable-dev-shm-usage')
firefoxOptions.add_argument('--ignore-certificate-errors')
firefoxOptions.add_argument('--allow-running-insecure-content')
firefoxOptions.binary = FIREFOXPATH

@st.experimental_singleton
def installff():
    os.system('sbase install geckodriver')
    os.system(
        'ln -s /home/appuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver.exe')
_ = installff()

def connect_to_google_sheet_chatbackup(name):
    google_key = 

    with open("google_key.json", "w") as outfile:
        json.dump(google_key, outfile)

    creds = gspread.service_account(filename="google_key.json")

    sh = creds.open("Статистика запросов")

    worksheet = sh.worksheet(name)

    return worksheet
def get_data():
    URL = 'https://seller.wildberries.ru'
    browser = webdriver.Firefox(executable_path=r'/home/appuser/venv/bin/geckodriver.exe', options=firefoxOptions)
    browser.get(URL)
    wait = WebDriverWait(browser, 15)
    number_ = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@data-find = 'phone-input']")))
    time.sleep(1)
    # TODO change number
    number_.send_keys("9156005045")
    time.sleep(1)
    button = browser.find_element(By.XPATH,
                                  "//span[@class = 'text--yon+U size-h6--1fGDJ isBold--xI37s isUpperCase--K1o9t']")
    browser.execute_script("arguments[0].click();", button)
    time.sleep(50)
    worksheet_ = connect_to_google_sheet_chatbackup(3)
    data_ = worksheet_.get_all_values()
    headers = data_.pop(0)
    df_ = get_as_dataframe(worksheet_, parse_dates=True,
                           usecols=[0], headers=0)
    code = df_['code'].tolist()[0].split('/')[-1]
    code = str(code)
    code_box = browser.find_element(By.XPATH, "//input[@autocomplete = 'off']")
    code_box.send_keys(code)
    time.sleep(20)
    # TODO Change user
    user_2 = browser.find_element(By.XPATH, "//button[@class = 'SelectInput__kUclwApgbL']")
    browser.execute_script("arguments[0].click();", user_2)
    check = browser.find_elements(By.XPATH,
                                  "//label[@class = 'Checkbox__xJ0jK0oJWs Checkbox--radio__dBCwMyX++J Checkbox--darkPurple__mPucK0b59h']")[
        -1]
    browser.execute_script("arguments[0].click();", check)
    browser.execute_script("arguments[0].click();", check)
    time.sleep(5)
    browser.get('https://seller.wildberries.ru/popular-search-requests')
    time.sleep(5)
    query = 'плать'
    query_input = browser.find_element(By.XPATH, "//input[@id='search']")
    query_input.send_keys(query)
    time.sleep(5)
    pages_num = browser.find_element(By.XPATH, "//input[@id='supply-pagination']")
    browser.execute_script("arguments[0].click();", pages_num)
    val_100 = \
    browser.find_elements(By.XPATH, "//span[@class='Text__CCxduTe6gB Text--h4__2tz_FOAqWW Text--black__2aiiAZwDOK']")[
        -1]
    browser.execute_script("arguments[0].click();", val_100)
    time.sleep(5)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    data = []
    tables = soup.find('table', {'class': 'Table__table__2tzi4nk-ul'})
    for i in tables:
        rows = i.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip().replace('\xa0', '') for ele in cols]
            data.append([ele for ele in cols if ele])
    for i in range(10):
        click_but = browser.find_elements(By.XPATH, "//button[@class='Pagination-icon-button__3GrEfjKw4D']")[-1]
        browser.execute_script("arguments[0].click();", click_but)
        time.sleep(4)
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        tables = soup.find('table', {'class': 'Table__table__2tzi4nk-ul'})
        for i in tables:
            rows = i.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip().replace('\xa0', '') for ele in cols]
                data.append([ele for ele in cols if ele])
    data = list(filter(None, data))
    now_date = datetime.datetime.now() + timedelta(days=5)
    now_date = now_date.strftime("%d.%m.%Y")
    df = pd.DataFrame(data, columns=['Запрос', 'Данные'])
    df['Дата'] = now_date
    worksheet_1 = connect_to_google_sheet_chatbackup('База данных')
    # сделать в ГС название колонок
    data_stat = worksheet_1.get_all_values()
    headers_ = data_stat.pop(0)
    df_from_db = pd.DataFrame(data_stat, columns=headers_)
    df_all = pd.concat([df_from_db, df])
    set_with_dataframe(worksheet_1, df_all)
    df_all = df_all.drop_duplicates(subset=['Дата', 'Запрос'])
    df_all['Данные'] = df_all['Данные'].astype('int')
    df_itog = df_all.sort_values(by=['Запрос', 'Дата'])
    df_itog['Изменение запросов в %'] = df_itog[['Запрос', 'Данные']].groupby('Запрос').pct_change()
    df_itog = df_itog.reset_index()
    del df_itog['index']
    worksheet_final = connect_to_google_sheet_chatbackup('Статистика запросов')
    worksheet_final.clear()
    set_with_dataframe(worksheet_final, df_itog)
    df_itog_ = df_itog.sort_values(by=['Изменение запросов в %'], ascending=False, na_position='last')
    df_itog_ = df_itog_.reset_index()
    del df_itog_['index']
    worksheet_final = connect_to_google_sheet_chatbackup('Группировка статистики по изменению запросов')
    worksheet_final.clear()
    set_with_dataframe(worksheet_final, df_itog_)

if __name__ == '__main__':
    installff()
    get_data()
