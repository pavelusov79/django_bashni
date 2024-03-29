import os
import datetime
import requests
import time

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


def parse_flats():
    client = MongoClient('127.0.0.1', 27017)
    db = client['flats_vl']
    db.flats.delete_many({'living_complex_name': 'Эко сити'})
    urls = ['https://жкэкосити.рф/interactive/?complex=jeko-siti&building=685', 
            'https://жкэкосити.рф/interactive/?complex=jeko-siti&building=321']
    service = Service(os.path.dirname(__file__) + '/geckodriver')
    options = Options()
    options.add_argument('--window-size=1200, 800')
    options.headless = True
    driver = Firefox(options=options, service=service)
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
    for url in urls:
        res = requests.get(url)
        if res.status_code == 200:
            driver.get(url)
            while True:
                time.sleep(3.5)
                height = driver.execute_script("return document.documentElement.scrollHeight")
                time.sleep(3.5)
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(3.5)
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                if new_height == height:
                    break
            time.sleep(4)
            q_ty = driver.find_element(By.CLASS_NAME, 'a-filter-tech__count-search')
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
                if url.split('=')[-1] == '685':
                    db_item['num_dom'] = 2
                else:
                    db_item['num_dom'] = 1
                
                db_item['num_fl'] = int(numbers[i].text[1:])
                db_item['_id'] = int(f'3{db_item["num_dom"]}{db_item["num_fl"]}')
                db_item['living_complex_name'] = "Эко сити"
                db_item['flat_type'] = types[i].text.split()[0]
                db_item['floor'] = int(floors[i].text)
                db_item['planning_url'] = drawings[i].get_attribute('src')
                db_item['price'] = int(prices[i].text.split()[0].replace(',', ''))
                db_item['flat_sq'] = float(sq[i].text.split()[0])
                db_item['flat_decor'] = 'Нет'
                path_to_media = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/flats')
                os.makedirs(f'{path_to_media}/{db_item["living_complex_name"]}', exist_ok=True)
                filename = f'{path_to_media}/{db_item["living_complex_name"]}/{db_item["planning_url"].split("/")[-1].replace("@", ".")}'
                db_item['path_to_planning'] = filename
                if not os.path.exists(filename):
                    r = requests.get(db_item["planning_url"])
                    with open(filename, 'wb') as f:
                        f.write(r.content)
                try:
                    db.flats.insert_one(db_item)   
                except DuplicateKeyError:
                    pass  
    time.sleep(2)
    driver.quit()

    logger_path = os.path.join(os.path.dirname(__file__), 'flats_logger.txt')
    with open(logger_path, 'a') as f:
        f.write(f"OK *** {datetime.datetime.now().strftime('%d.%m.%y %H:%M')} *** спарсено {db.flats.count_documents({'living_complex_name': 'Эко сити'})} квартир с parsing_ecocity.py\n")
    
    return db



parse_flats()
                
