import json
import time
import requests
from bs4 import BeautifulSoup
import lxml
from selenium.common import NoSuchElementException
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By

# функция для парсинга с помощью Selenium

def selenium_parse(url: str) -> list:
    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('--headless')
    with webdriver.Chrome(options=options_chrome) as browser:
        browser.get(url)
        time.sleep(2)
        data = {}
        all_data = []
        vacans = browser.find_elements(By.CLASS_NAME, 'vacancy-serp-item-body')
        for vacan in vacans:
            data['name'] = vacan.find_element(By.CSS_SELECTOR, 'a.serp-item__title').text
            data['link'] = vacan.find_element(By.CSS_SELECTOR, '.serp-item__title').get_attribute('href')
            try:
                data['salary'] = vacan.find_element(By.CSS_SELECTOR, '.bloko-header-section-2').text
                data['salary'] = data['salary'].replace(u'\u202F', ' ')
                data['salary'] = data['salary'].replace(u'\u20bd', 'RUB')
            except NoSuchElementException:
                data['salary'] = 'UKWN'
            data['company'] = vacan.find_element(By.CSS_SELECTOR, '.vacancy-serp-item__meta-info-company a').text
            data['company'] = data['company'].replace(u'\xa0', ' ')
            data['city'] = vacan.find_element(By.CSS_SELECTOR, '[data-qa=vacancy-serp__vacancy-address]').text
            all_data.append(data.copy())
    return all_data

# функция, реализующая парсинг с помощью Requests. Внутри также чистка от символов,
# на которых спотыкается запись в json. С помощью ловли ошибок ловлю ситуацию, когда з/п не указана

def request_parse(all_vacans: list) -> list:
    data = {}
    all_data = []
    for vacan in all_vacans:
        if vacan.select_one('.bloko-header-section-2') != None:
            if vacan.select_one('.bloko-header-section-2').text.find('$') != -1:
                data['name'] = vacan.select_one('.vacancy-serp-item-body a.serp-item__title').text
                data['link'] = vacan.select_one('.vacancy-serp-item-body a.serp-item__title').attrs['href']
                try:
                    data['salary'] = vacan.select_one('.bloko-header-section-2').text
                    data['salary'] = data['salary'].replace(u'\u202F', ' ')
                    data['salary'] = data['salary'].replace(u'\u20bd', 'RUB')
                except AttributeError:
                    data['salary'] = 'UKWN'
                data['company'] = vacan.select_one('.vacancy-serp-item__meta-info-company a').text
                data['company'] = data['company'].replace(u'\xa0', ' ')
                data['city'] = vacan.select_one('[data-qa=vacancy-serp__vacancy-address]').text
                all_data.append(data.copy())
    return all_data