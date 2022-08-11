import os
import datetime
import requests

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError 
from lxml import html


def parse_flats():
    client = MongoClient('127.0.0.1', 27017)
    db = client['flats_vl']
    db.flats.delete_many({'living_complex_name': 'Восточный луч'})
    url = 'https://vlzu.ru/apartments'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        dom = html.fromstring(res.text)
        last_page_num = dom.xpath('//a[contains(@class, "Paginator_btn")]/text()')[-1]
        for i in range(1, int(last_page_num) + 1):
            r = requests.get(f'https://vlzu.ru/apartments?page={i}', headers=headers)
            if r.status_code == 200:
                d = html.fromstring(r.text)
                # drawings = d.xpath('//div[contains(@class, "CardBox_image")]/img/@src')
                links = d.xpath('//a[contains(@class, "CardBox_link")]/@href')
                prices = d.xpath('//div[contains(@class, "CardBox_priceBox")]/div[contains(@class, "CardBox_value")]/span/text()')
                for i in range(len(links)):
                    r = requests.get(f'https://vlzu.ru{links[i]}')
                    if r.status_code == 200:
                        db_item = {}
                        dom = html.fromstring(r.text)
                        db_item['living_complex_name'] = "Восточный луч"
                        db_item['price'] = int(prices[i].replace(' ', ''))
                        db_item['flat_type'] = dom.xpath('//div[contains(@class, "ApartmentInfo_name")]//span/text()')[0]
                        db_item['num_dom'] = int(dom.xpath('//div[contains(@class, "ApartmentInfo_prop_value")]/text()')[4])
                        db_item['num_fl'] = int(dom.xpath('//div[contains(@class, "ApartmentInfo_prop_value")]/text()')[2])
                        db_item['_id'] = int(f'2{db_item["num_dom"]}{db_item["num_fl"]}')
                        fl_sq = dom.xpath('//div[contains(@class, "ApartmentInfo_name")]//span/text()')[-2]
                        db_item['flat_sq'] = float(fl_sq.replace(',', '.'))
                        db_item['floor'] = int(dom.xpath('//div[contains(@class, "ApartmentInfo_prop_value")]/text()')[3])
                        db_item['planning_url'] = dom.xpath('//div[contains(@class, "CardBox_image")]/img/@src')[0]
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

    logger_path = os.path.join(os.path.dirname(__file__), 'flats_logger.txt')
    with open(logger_path, 'a') as f:
        f.write(f"OK *** {datetime.datetime.now().strftime('%d.%m.%y %H:%M')} *** спарсено {db.flats.count_documents({'living_complex_name': 'Восточный луч'})} квартир сparsing_vostluch.py\n")

    return db


parse_flats()
                
