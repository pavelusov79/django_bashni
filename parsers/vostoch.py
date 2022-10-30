import requests
import os
import time
import datetime

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium_stealth import stealth

from pprint import pprint


def parse_flats():
    client = MongoClient('127.0.0.1', 27017)
    db = client['flats_vl']
    db.flats.delete_many({'living_complex_name': 'Восточный'})
    urls = [
        'https://xn--2020-z5dst.xn--p1ai/component/megaplan/?view=megaplan&id=4',
        'https://xn--2020-z5dst.xn--p1ai/component/megaplan/?view=megaplan&id=20',
        'https://xn--2020-z5dst.xn--p1ai/component/megaplan/?view=megaplan&id=41',
        'https://xn--2020-z5dst.xn--p1ai/component/megaplan/?view=megaplan&id=59',
        'https://xn--2020-z5dst.xn--p1ai/component/megaplan/?view=megaplan&id=78'
    ]
    for url in urls:
        print(url)
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        # options.add_argument('start-maximized')
        options.add_argument('--headless')
        options.add_argument('--window-size=1920, 950') #1800x900, 1360X768, 1800x980, 1900x1100, 1920x1000
        driver = webdriver.Chrome(options=options, service=service)
        driver.get(url)
        driver.implicitly_wait(5)
        f = driver.find_element(By.XPATH, '//div[@class="new"]/*[name()="svg"]')
        els = f.find_elements(By.XPATH, './*[name()="path"]')
        for elem in els:
            ActionChains(driver).move_to_element(elem).click().perform()
            try:
                fr = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//iframe[@class="mfp-iframe"]')))
                # fr = driver.find_element(By.XPATH, '//iframe[@class="mfp-iframe"]')
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(fr))
                ActionChains(driver).send_keys(Keys.DOWN).perform()
                try:
                    flats = WebDriverWait(driver, 8).until(EC.presence_of_all_elements_located((By.XPATH, '//*[name()="path" and @fill="#3ba108"]')))
                except Exception:
                    driver.switch_to.default_content()
                    btn = driver.find_element(By.XPATH, '//button[@class="mfp-close"]')
                    btn.click()
                    continue
                time.sleep(1)
                fl_paths = {}
                for i in range(len(flats)):
                    fl_paths[i] = flats[i].get_attribute('id')
                for item in range(len(flats)):
                    db_item = {}
                    path_el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[name()="path" and @id="{fl_paths[item]}"]')))
                    # ActionChains(driver).move_to_element(driver.find_element(By.XPATH, f'//*[name()="path" and @id="{fl_paths[item]}"]')).click().perform()
                    ActionChains(driver).send_keys(Keys.DOWN).perform()
                    time.sleep(0.5)
                    ActionChains(driver).send_keys(Keys.DOWN).perform()
                    time.sleep(1)
                    ActionChains(driver).move_to_element(path_el).click().perform()
                    driver.switch_to.default_content()
                    time.sleep(1)
                    frame = driver.find_element(By.XPATH, '//iframe[@class="mfp-iframe"]')
                    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(frame))
                    try:
                        if url == 'https://xn--2020-z5dst.xn--p1ai/component/megaplan/?view=megaplan&id=20':
                            num_dom = driver.find_element(By.XPATH, '//div[@class="apartment-details"]//em').text.split(',')[-1].split()[-4]
                        else:
                            num_dom = driver.find_element(By.XPATH, '//div[@class="apartment-details"]//em').text.split(',')[-1].split()[-3]
                    except Exception:
                        if flats[item] == flats[-1]:
                            driver.switch_to.default_content()
                            btn = driver.find_element(By.XPATH, '//button[@class="mfp-close"]')
                            btn.click()
                            continue
                        else:
                            continue
                    db_item['num_dom'] = int(num_dom)
                    num_fl = driver.find_element(By.XPATH, '//div[@class="apartment-info-box"]/h1').text.split()[1]
                    db_item['num_fl'] = int(num_fl)
                    db_item['_id'] = int(f'201{db_item["num_dom"]}{db_item["num_fl"]}')
                    db_item['flat_decor'] = 'Нет'
                    fl_sq = driver.find_element(By.XPATH, '//div[@class="apartment-details"]//strong').text.split()[0]
                    db_item['flat_sq'] = float(fl_sq)
                    if url == 'https://xn--2020-z5dst.xn--p1ai/component/megaplan/?view=megaplan&id=20':
                        floor = driver.find_element(By.XPATH, '//div[@class="apartment-details"]//em').text.split(',')[-1].split()[-2]
                    else:
                        floor = driver.find_element(By.XPATH, '//div[@class="apartment-details"]//em').text.split(',')[-1].split()[-1]
                    db_item['floor'] = int(floor)
                    # zhk_name = driver.find_element(By.XPATH, '//div[@class="apartment-details"]//em').text.split(',')[0].split()[-1].replace('"', '')
                    db_item['living_complex_name'] = 'Восточный'
                    fl_status = driver.find_element(By.XPATH, '//div[@class="status_kom"]').text
                    db_item['status'] = fl_status
                    fl_type = driver.find_element(By.XPATH, '//div[@class="apartment-details"]/p').text.split('\n')[-1].split()[-1]
                    db_item['flat_type'] = fl_type
                    price = driver.find_element(By.XPATH, '//div[@class="apartment-details"]//span[@style]').text
                    db_item['price'] = int(price.replace('руб.', '').replace(' ', '').strip())
                    img_plan = driver.find_element(By.XPATH, '//img[contains(@class, "plan-pic")]').get_attribute('src')
                    db_item['planning_url'] = img_plan
                    path_to_media = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/flats')
                    os.makedirs(f'{path_to_media}/{db_item["living_complex_name"]}', exist_ok=True)
                    filename = f'{path_to_media}/{db_item["living_complex_name"]}/{db_item["planning_url"].split("/")[-1].replace("@", ".")[-18:]}'
                    db_item['path_to_planning'] = filename
                    if not os.path.exists(filename):
                        r = requests.get(db_item["planning_url"])
                        with open(filename, 'wb') as f:
                            f.write(r.content)
                    try:
                        db.flats.insert_one(db_item)
                    except DuplicateKeyError:
                        print('duplicate found')
                        print(db.flats.find_one({'_id': db_item['_id']}))
                        try:
                            if db_item['living_complex_name'] != 'Восточный':
                                db_item['_id'] = f'2{db_item["_id"]}'
                                db.flats.insert_one(db_item)
                        except DuplicateKeyError:
                            print('duplicate 2!')
                    rev_link = driver.find_element(By.XPATH, '//a[@class="pdf-link"]')
                    if item != len(flats) - 1:
                        rev_link.click()
                        # driver.switch_to.default_content()
                        # time.sleep(0.5)
                    else:
                        driver.switch_to.default_content()
                        btn = driver.find_element(By.XPATH, '//button[@class="mfp-close"]')
                        btn.click()
                        time.sleep(1)
                    # pprint(db_item)
                    # print('-----------------------------')
            except TimeoutException:
                continue
        print()
        time.sleep(1)
        driver.quit()
    logger_path = os.path.join(os.path.dirname(__file__), 'flats_logger.txt')
    with open(logger_path, 'a') as f:
        f.write(
            f"OK *** {datetime.datetime.now().strftime('%d.%m.%y %H:%M')} *** спарсено {db.flats.count_documents({'living_complex_name': 'Восточный'})} квартир с vostoch.py\n")
    print('script done!')
    return db


parse_flats()
