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


# def parse_flats():
#     # client = MongoClient('127.0.0.1', 27017)
#     # db = client['flats_vl']
#     # db.flats.delete_many({'living_complex_name': 'Новожилово'})
#     # db.flats.delete_many({'living_complex_name': 'Восточный'})
#     # db.flats.delete_many({'living_complex_name': 'Аякс'})
#     urls = [
#         'https://vladivostok.domclick.ru/search?deal_type=sale&category=living&offset=0&complex_ids=116786&complex_name=%D0%96%D0%9A%20%22%D0%9D%D0%BE%D0%B2%D0%BE%D0%B6%D0%B8%D0%BB%D0%BE%D0%B2%D0%BE%22',
#
#     ]
#     for url in urls:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'Cookie': 'ftgl_cookie_id=2379a73d7899a190d1942822739ca770; _ym_uid=166495565813980988; _ym_d=1664955658; iap.uid=b383ee82ee4649c483fa8cf0db59c397; ___dmpkit___=9b24c938-278e-400a-ab34-aeb30cf6a6c0; _gcl_au=1.1.586041584.1664955659; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; tmr_lvid=a476280283486dfc2e420458c7f3a18d; tmr_lvidTS=1664955662092; adtech_uid=98b877f8-e1e0-420a-bda0-de24e53a760b%3Adomclick.ru; top100_id=t1.4513750.1621206774.1664955662629; RETENTION_COOKIES_NAME=c82f5396d31a462188236f7afe96bddd:RyQsoarR-fqeYhasUpr7BZRpAVg; sessionId=3cbb971f2aa84acfa2772e9912f4eee6:zK4cB7W7SRJC-9naD2GuAfFsaPk; UNIQ_SESSION_ID=c37cc77adc90426592579d615a8a5f65:Yod9pbbuMN90VHNlrbMpsIIUYvk; adrcid=AMFj0LldRoMMsCnB4Y6BswQ; currentRegionGuid=619fd4a7-2e28-4d8e-b333-d1c7324c94be; currentLocalityGuid=09b74a8a-e195-493d-b776-fb00c9b763bd; ns_session=54e0c66e-b04d-5928-9ac1-95b2ecd4a8ff; currentSubDomain=vladivostok; regionName=09b74a8a-e195-493d-b776-fb00c9b763bd:%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%B2%D0%BE%D1%81%D1%82%D0%BE%D0%BA; _ym_isad=2; _gid=GA1.2.1798663704.1665878103; dtCookie=v_4_srv_7_sn_C10AD63F8FACF2B1195A254C3788CB62_perc_100000_ol_0_mul_1_app-3Aa90421fc39b1dbac_0_app-3Aca312da39d5a5d07_1_app-3A37d82a95eb231749_0_rcs-3Acss_0; cookieAlert=1; qrator_jsid=1665899836.527.8IadWDdKS2n7cm2F-r159un57aq0u9niai9gv4oiudk06hdq1; showComparisonHint=1; _ga=GA1.2.1278772854.1664955659; last_visit=1665880750074%3A%3A1665916750074; tmr_detect=0%7C1665916752462; _ga_NP4EQL89WF=GS1.1.1665919211.6.0.1665919211.60.0.0; _visitId=79307a38-0ba9-4bf5-822e-0e13c74fb092-6d898147f1be2b28; CAS_ID=4364551; CAS_ID_SIGNED=eyJleHAiOiAxNjczODAzMzQyLCAidGd0IjogIlRHVC03ODY3MS01WDJHeTFvdjF1akhmTVJWS3g5Q3NsTlRMcGR1YVVNZk9KNEpnU1d4UW1ORUtrQVpiUC1jYXMubGMiLCAiY2FzSWQiOiA0MzY0NTUxLCAibG9naW5UeXBlIjogIkRFRkFVTFQiLCAibG9naW5UaW1lIjogMTY2NTkxOTM0Mn0=.nt2XJ/iSR9FYJyqBHHonn4brdKlb0f/KHs6ED4fQnzwMFWTNt2M3G2LMG+s8n6Ey3UIZOZFUFCi29cKnRciL9V1XlDcm3cI/JrOyecir12o2fWy4GGa9M3KE2lfgz2swuRYpKtj/7sUWqqafPYHGOEdCGuRPnd8pTTC0sXTi/xo=; _sa=SA1.3a52094c-0d9f-4272-a5a6-ad858923f2ea.1665919419; t3_sid_4513750=s1.706839908.1665919211807.1665919668533.7.12.168; tmr_reqNum=24',
#         }
#         res = requests.get(url, headers=headers)
#         if res.status_code == 200:
#             dom = html.fromstring(res.text)
#             links = dom.xpath('//a[@data-test="product-snippet-property-offer"]/@href')
#             for link in links:
#                 link_res = requests.get(link, headers=headers)
#                 if link_res.status_code == 200:
#                     dom = html.fromstring(link_res.text)
#                     pagination = dom.xpath('//div[@data-test-id="pagination"]/button/text()')[-1]
#                     if not pagination:
#                         flats = dom.xpath('//div[@class="flatSelection_flatCard"]')
#                         zhk_name = dom.xpath('//a[@class="sc_innerDomclickLink sc_innerDomclickLink--link"]/text()')[0]
#                         for flat in flats:
#                             db_item = {}
#                             price = flat.xpath('.//span[@class="flatSelection_cardPrice"]/text()')[0].strip().replace(' ', '')
#                             area = flat.xpath('.//span[@class="flatSelection_infoItemValue"]/text()')[0]
#                             floor = flat.xpath('.//span[@class="flatSelection_infoItemValue"]/text()')[2].split('/')[0]
#                             fl_num = flat.xpath('.//span[@class="flatSelection_infoItemValue"]/text()')[-1]
#                             db_item['num_fl'] = int(fl_num)
#                             db_item['_id'] = int(f'200{db_item["num_fl"]}')
#                             db_item['floor'] = int(floor)
#                             db_item['flat_sq'] = float(area)
#                             db_item[''] = int(price)
#                             if re.search(r'Новожилово', zhk_name):
#                                 db_item['living_complex_name'] = 'Новожилово'
#                                 db_item['num_dom'] = 1
#                                 db_item['flat_decor'] = 'Нет'
#                     else:
#                         service = Service(executable_path=ChromeDriverManager().install())
#                         options = Options()
#                         options.add_argument("--user-data-dir=chrome-data")
#                         options.add_argument('start-maximized')
#                         # options.headless = True
#                         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#                         options.add_experimental_option('useAutomationExtension', False)
#                         driver = webdriver.Chrome(options=options, service=service)
#                         driver.get(link)
#                         pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
#                         driver.quit()
#                         driver = webdriver.Chrome(options=options, service=service)
#                         cookies = pickle.load(open("cookies.pkl", "rb"))
#                         driver.add_cookie({'name': cookies[0]['name'], 'value': cookies[0]['value'], 'domain': 'domclick.ru'})
#                         # for cookie in cookies:
#                         #     driver.add_cookie({'domain': cookie['domain'], 'name': cookie['name'], 'value': cookie['value']})
#                         stealth(driver,
#                                 user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
#                                 languages=["en-US", "en"],
#                                 vendor="Google Inc.",
#                                 platform="Win32",
#                                 webgl_vendor="Intel Inc.",
#                                 renderer="Intel Iris OpenGL Engine",
#                                 fix_hairline=True,
#                                 )
#                         time.sleep(1)
#                         pagin_items = driver.find_elements(By.XPATH, '//button[@class="sc_pagination_button"]')
#                         zhk_name = driver.find_element(By.XPATH, '//a[@class="sc_innerDomclickLink sc_innerDomclickLink--link"]').text
#                         for item in range(len(pagin_items) + 1):
#                             flats = driver.find_elements(By.XPATH, '//div[@class="flatSelection_flatCard"]')
#                             for flat in flats:
#                                 db_item = {}
#                                 price = flat.find_element(By.XPATH, './/span[@class="flatSelection_cardPrice"]').text[0].strip().replace(' ', '')
#                                 area = flat.find_element(By.XPATH, './/span[@class="flatSelection_infoItemValue"]').text[0]
#                                 floor = flat.find_element(By.XPATH, './/span[@class="flatSelection_infoItemValue"]').text[2].split('/')[0]
#                                 fl_num = flat.find_element(By.XPATH, './/span[@class="flatSelection_infoItemValue"]').text[-1]
#                                 db_item['num_fl'] = int(fl_num)
#                                 db_item['_id'] = int(f'200{db_item["num_fl"]}')
#                                 db_item['floor'] = int(floor)
#                                 db_item['flat_sq'] = float(area)
#                                 db_item[''] = int(price)
#                                 if re.search(r'Новожилово', zhk_name):
#                                     db_item['living_complex_name'] = 'Новожилово'
#                                     db_item['num_dom'] = 1
#                                     db_item['flat_decor'] = 'Нет'
#                                 pprint(db_item)
#                                 print('----------------------')
#                             if item != int(pagin_items[-1].text):
#                                 pagin_items[item].click()
#                             driver.quit()
#                             print()


def parse_flats():
    client = MongoClient('127.0.0.1', 27017)
    db = client['flats_vl']
    db.flats.delete_many({'living_complex_name': 'Аякс'})
    urls = [
        'https://xn--80almb9a8e.xn--p1ai/buy'
    ]
    for url in urls:
        service = Service(executable_path=ChromeDriverManager().install())
        # service = Service(executable_path='/home/pavel/Документы/NEW_DJUNGO_PROJECTS/bashni_new/parsers/chromedriver')
        options = Options()
        # options.add_argument('start-maximized')
        options.add_argument('--headless')
        options.add_argument('--window-size=1920, 950') #1800x900, 1360X768, 1800x980, 1900x1100, 1920x1000
        driver = webdriver.Chrome(options=options, service=service)
        driver.get(url)
        print(url)
        driver.implicitly_wait(5)
        f = driver.find_element(By.XPATH, '//div[@class="new"]/*[name()="svg"]')
        els = f.find_elements(By.XPATH, './*[name()="path"]')
        for el in els:
            ActionChains(driver).move_to_element(el).click().perform()
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
                    ActionChains(driver).send_keys(Keys.DOWN).perform()
                    time.sleep(0.5)
                    ActionChains(driver).move_to_element(path_el).click().perform()
                    driver.switch_to.default_content()
                    time.sleep(1)
                    frame = driver.find_element(By.XPATH, '//iframe[@class="mfp-iframe"]')
                    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(frame))
                    fl_info = driver.find_element(By.XPATH, '//div[@class="apartment-info-box"]/h1').text.split('\n')[0]
                    num_dom = fl_info.split(' ')[1]
                    db_item['num_dom'] = int(num_dom)
                    num_fl = fl_info.split(' ')[-1]
                    db_item['num_fl'] = int(num_fl)
                    db_item['_id'] = int(f'200{db_item["num_dom"]}{db_item["num_fl"]}')
                    db_item['flat_decor'] = 'Нет'
                    fl_sq = driver.find_element(By.XPATH, '//div[@class="apartment-details"]//strong').text.split()[0]
                    db_item['flat_sq'] = float(fl_sq)
                    floor = driver.find_element(By.XPATH, '//div[@class="apartment-details"]//em').text.split(',')[-1].split()[-1]
                    db_item['floor'] = int(floor)
                    zhk_name = driver.find_element(By.XPATH, '//div[@class="apartment-details"]//em').text.split(',')[0].split()[-1].replace('"', '')
                    db_item['living_complex_name'] = zhk_name
                    fl_status = driver.find_element(By.XPATH, '//div[@class="status_kom"]').text
                    db_item['status'] = fl_status
                    fl_type = driver.find_element(By.XPATH, '//div[@class="apartment-details"]/p').text.split('\n')[-1].split()[-1]
                    db_item['flat_type'] = fl_type
                    db_item['price'] = 0
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
                            if db_item['living_complex_name'] != 'Аякс':
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
        time.sleep(1)
        driver.quit()
    logger_path = os.path.join(os.path.dirname(__file__), 'flats_logger.txt')
    with open(logger_path, 'a') as f:
        f.write(
            f"OK *** {datetime.datetime.now().strftime('%d.%m.%y %H:%M')} *** спарсено {db.flats.count_documents({'living_complex_name': 'Аякс'})} квартир с ayaks.py\n")
    return db


parse_flats()
