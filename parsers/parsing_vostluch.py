from pymongo import MongoClient
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import os
import datetime
import pytz
import requests
import time


def parse_flats():
    client = MongoClient('127.0.0.1', 27017)
    db = client['flats_vl']
    db.flats.delete_many({'living_complex_name': 'ЖК Восточный луч'})
    urls = [
            'https://vlzu.ru/bronirovanie/?jk=vostochnyj-luch.-2-ochered&building=943',
            'https://vlzu.ru/bronirovanie/?jk=vostochnyj-luch&building=769', 
            'https://vlzu.ru/bronirovanie/?jk=vostochnyj-luch&building=772',
            'https://vlzu.ru/bronirovanie/?jk=vostochnyj-luch&building=788', 
            'https://vlzu.ru/bronirovanie/?jk=vostochnyj-luch&building=790',
            'https://vlzu.ru/bronirovanie/?jk=vostochnyj-luch&building=791',
            'https://vlzu.ru/bronirovanie/?jk=vostochnyj-luch&building=792']
    service = Service(os.path.dirname(__file__) + '/geckodriver')
    options = Options()
    options.add_argument('--window-size=1200, 800')
    options.headless = True
    driver = Firefox(options=options, service=service)
    for url in range(len(urls)):
        driver.get(urls[url])
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-elementor-type="footer"]')))
        q_ty = driver.find_element(By.XPATH, '//div[@class="a-filter-tech__count-search"]')
        types = driver.find_elements(By.CLASS_NAME, 'a-table-komn')
        drawings = driver.find_elements(By.XPATH, '//div[@class="a-table-img"]/img')
        numbers = driver.find_elements(By.CLASS_NAME, 'a-table-num')
        floors = driver.find_elements(By.CLASS_NAME, 'a-table-etazh')
        sq = driver.find_elements(By.CLASS_NAME, 'a-table-pl')
        prices = driver.find_elements(By.CLASS_NAME, 'a-table-price')
        print(q_ty.text)
        print('els= ', len(types))
        for i in range(len(types)):
            db_item = {}
            if url == 0:
                db_item['num_dom'] = 1
            elif url == 1:
                db_item['num_dom'] = 5
            elif url == 2:
                db_item['num_dom'] = 6
            elif url == 3:
                db_item['num_dom'] = 7
            elif url == 4:
                db_item['num_dom'] = 8
            elif url == 5:
                db_item['num_dom'] = 9
            else:
                db_item['num_dom'] = 10
            db_item['num_fl'] = int(numbers[i].text[1:])
            db_item['_id'] = int(f'2{db_item["num_dom"]}{db_item["num_fl"]}')
            db_item['living_complex_name'] = "ЖК Восточный луч"
            db_item['flat_type'] = types[i].text.split()[0]
            db_item['floor'] = int(floors[i].text)
            db_item['planning_url'] = drawings[i].get_attribute('src')
            db_item['price'] = int(prices[i].text.split()[0].replace(',', ''))
            db_item['flat_sq'] = float(sq[i].text.split()[0])
            db_item['flat_decor'] = 'Нет'
            os.makedirs(f'{os.path.dirname(__file__)}/images/vostoch_luch/{db_item["num_dom"]}/', exist_ok=True)
            filename = f'{os.path.dirname(__file__)}/images/vostoch_luch/{db_item["num_dom"]}/{db_item["planning_url"].split("/")[-1].replace("@", ".")}'
            db_item['path_to_planning'] = filename
            if os.path.exists(filename):
                os.remove(filename)
            r = requests.get(db_item["planning_url"])
            with open(filename, 'wb') as f:
                f.write(r.content)
            db.flats.insert_one(db_item)     
    driver.close()

    logger_path = os.path.join(os.path.dirname(__file__), 'flats_logger.txt')
    with open(logger_path, 'a') as f:
        f.write(f"OK *** {datetime.datetime.now(pytz.timezone('Asia/Vladivostok')).strftime('%d.%m.%y %H:%M')} *** спарсено {db.flats.count_documents({'living_complex_name': 'ЖК Восточный луч'})} квартир сparsing_vostluch.py\n")

    return db


parse_flats()
                
