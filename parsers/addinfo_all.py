from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from lxml import html
import requests
import os
import datetime
import pytz
import wget
from PIL import Image, UnidentifiedImageError
from pprint import pprint


def get_urls():
    url_links = []
    url = 'https://наш.дом.рф/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA?objStatus=0&residentialBuildings=1&place=0-26&page=0&limit=100'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        dom = html.fromstring(res.text)
        p = dom.xpath('//a[@class="pagination-item"]/text()')
        links = dom.xpath('//a[contains(@class, "styles__Address")]/@href')
        for link in links:
            url_links.append(link)
        s = Service(os.path.dirname(__file__) + '/geckodriver')
        # options = Options()
        # options.add_argument('--window-size=1200, 800')
        # options.headless = True
        driver = Firefox(service=s)
        for i in range(1, int(p[-1])):
            link = f'https://наш.дом.рф/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA?objStatus=0&residentialBuildings=1&place=0-26&page={i}&limit=100'
            driver.get(link)
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//li/a")))
            objs = driver.find_elements(By.XPATH, '//a[contains(@class, "Address")]')
            print(len(objs))
            for item in objs:
                url_links.append(item.get_attribute('href'))  
        driver.close()
    print(len(url_links))
    return url_links


def parse():
    client = MongoClient('127.0.0.1', 27017)
    db = client['nashdom_vl_db']
    main_collection = db['main_collection']
    url_links = get_urls()
    s = Service(os.path.dirname(__file__) + '/geckodriver')
    options = Options()
    options.add_argument('--window-size=1200, 800')
    options.headless = True
    driver = Firefox(options=options, service=s)
    for url in url_links:
        db_item = {}
        driver.get(url)
        try:
            confirm_cookie = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'styles__ButtonContentWrapper-sc-')]")))
            confirm_cookie.click()
        except Exception:
            pass
        dom_id = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//p[contains(@class, "styles__Id-sc-")]'))).text.split(':')[-1]
        print(dom_id.strip())
        db_item['_id'] = int(dom_id)
        stroy_imgs = WebDriverWait(driver, 12).until(EC.presence_of_all_elements_located((By.XPATH, '//h4[contains(@class, "styles__Date")]')))[:3]
        d_img = {}
        el = main_collection.find_one({'_id': db_item['_id']})
        for i in range(len(stroy_imgs)):
            if stroy_imgs[i].text not in el['build_imgs'].keys():
                stroy_imgs[i].click() 
                photos = driver.find_elements(By.XPATH, '//button[contains(@class, "styles__Thumbnail")]')[:3]
                os.makedirs(f'{os.path.dirname(__file__)}/images/{dom_id}/building/{stroy_imgs[i].text}/', exist_ok=True)
                for photo in photos:
                    filename = f'{os.path.dirname(__file__)}/images/{dom_id}/building/{stroy_imgs[i].text}/{photo.get_attribute("src").split("/")[-1].split("-")[0]}.jpg'
                    if not os.path.exists(filename):
                        try:
                            wget.download(photo.get_attribute("src"), out=filename)
                        except Exception:
                            pass
                #resize images
                path_to_dir = os.path.join(os.path.dirname(__file__), 'images', dom_id, 'building', stroy_imgs[i].text)
                files = os.listdir(path_to_dir)
                img_list = []
                for file in files:
                    if file.split('.')[-1] == 'jpg':
                        try:
                            org_img = Image.open(os.path.join(path_to_dir, file))
                            width, height = org_img.size
                            if width > 640:
                                width_ratio = round(640 / width * 100)
                                if org_img.mode == 'RGBA' or org_img.mode == 'P':
                                    org_img = org_img.convert('RGB')
                                org_img.save(os.path.join(path_to_dir, file), quality=width_ratio)
                            img_list.append(os.path.join(path_to_dir, file))
                        except UnidentifiedImageError:
                            pass
                d_img[f'{stroy_imgs[i].text}'] = img_list
                driver.find_element(By.XPATH, '//button[contains(@class, "styles__CloseButton")]').click()
                db_item['build_imgs'] = d_img
        if d_img:
            main_collection.update_one({'_id': db_item["_id"]},
                                    {'$set': {'build_imgs': d_img}})
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.TAG_NAME, 'li')))
        driver.find_elements(By.TAG_NAME, 'li')[1].click()
        docs = driver.find_elements(By.XPATH, '//div[contains(@class, "styles__Tab")]/button[contains(@class, "styles__ButtonContainer")]')[1:3]
        doc_list = []
        for i in range(len(docs)):
            docs[i].click()
            doc_containers = driver.find_elements(By.XPATH, '//a/div[contains(@class, "styles__Row-sc-")]')
            for el in doc_containers:
                el_dict = {}
                el_dict['name'] = el.find_element(By.XPATH, './/h4[contains(@class, "Primary")]').text
                el_date = el.find_element(By.XPATH, './/span[contains(@class, "Date")]').text
                el_dict['date'] = datetime.datetime.strptime(el_date, "%d.%m.%Y")
                el_dict['link'] = el.find_element(By.XPATH, './/a[@download]').get_attribute('href')
                doc_list.append(el_dict) 
        db_item['documents'] = doc_list
        
        main_collection.update_one({'_id': db_item["_id"]},
                                        {'$set': {'documents': doc_list}})
      
    driver.close()  

    logger_path = os.path.join(os.path.dirname(__file__), 'nashdom_logger.txt')
    with open(logger_path, 'a') as f:
        f.write(f"OK *** {datetime.datetime.now(pytz.timezone('Asia/Vladivostok')).strftime('%d.%m.%y %H:%M')} *** addinfo_all.py\n") 

    return db


parse()
