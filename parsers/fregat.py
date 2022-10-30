from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from lxml import html
import requests
import os
import wget
import datetime


def parse_flats():
    client = MongoClient('127.0.0.1', 27017)
    db = client['flats_vl']
    db.flats.delete_many({'living_complex_name': 'Фрегат 2'})
    urls = ['https://fregat2.ru/flats/nejbuta-dom-7/', 'https://fregat2.ru/flats/nejbuta-dom-6/', 'https://fregat2.ru/flats/nejbuta-dom-8/', 'https://fregat2.ru/flats/nejbuta-dom-5/']
    for url in urls:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            dom = html.fromstring(res.text)
            floors = dom.xpath('//div[contains(@class, "homes__number")]')[1:]
            rows = dom.xpath('//div[contains(@class, "homes__row")]')
            for el in range(len(rows)):
                for i in range(len(rows[el])):
                    if rows[el][i].xpath('./@href'):
                        db_item = {}
                        num_dom = int(dom.xpath('//h1/text()')[0].split()[-1])
                        fl_id = int(f'1{num_dom}{el}{i}')
                        db_item['_id'] = fl_id
                        db_item['living_complex_name'] = 'Фрегат 2'
                        db_item['num_dom'] = num_dom
                        db_item['num_fl'] = ''
                        url_link =rows[el][i].xpath('./@href')[0]
                        fl_type = rows[el][i].xpath('./text()')[0].strip()
                        db_item['flat_type'] = fl_type
                        plan_url = rows[el][i].xpath('./@data-plan')[0]
                        db_item['planning_url'] = plan_url
                        path_to_media = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/flats')
                        os.makedirs(f'{path_to_media}/{db_item["living_complex_name"]}', exist_ok=True)
                        filename = f'{path_to_media}/{db_item["living_complex_name"]}/{plan_url.split("/")[-1]}'
                        db_item['path_to_planning'] = filename
                        if not os.path.exists(filename):
                            try:
                                wget.download(plan_url, out=filename)
                                # r = requests.get(plan_url)
                                # with open(filename, 'wb') as f:
                                #     f.write(r.content)
                            except Exception:
                                db_item['path_to_planning'] = ''
                        fl_price = int(rows[el][i].xpath('./@data-price')[0].replace(' ', ''))
                        db_item['price'] = fl_price
                        fl_sq = float(rows[el][i].xpath('./@data-plow')[0])
                        db_item['flat_sq'] = fl_sq
                        floor = int(floors[el].text)
                        db_item['floor'] = floor
                        res = requests.get(url_link, headers=headers)
                        if res.status_code == 200:
                            dom = html.fromstring(res.text)
                            try:
                                decor = dom.xpath('//td/text()')[3].strip()
                                db_item['flat_decor'] = decor
                            except IndexError:
                                db_item['flat_decor'] = 'Да'
                                print(f'*******{url_link}*********')
                        try:
                            db.flats.insert_one(db_item)
                        except DuplicateKeyError:
                            print('duplicate found')
                            print(db.flats.find_one({'_id': db_item['_id']}))
                            try:
                                db_item['_id'] = f'100{db_item["_id"]}'
                                db.flats.insert_one(db_item)
                            except DuplicateKeyError:
                                print('duplicate 2!')
                                                  
    logger_path = os.path.join(os.path.dirname(__file__), 'flats_logger.txt')
    with open(logger_path, 'a') as f:
        f.write(f"OK *** {datetime.datetime.now().strftime('%d.%m.%y %H:%M')} *** спарсено {db.flats.count_documents({'living_complex_name': 'Фрегат 2'})} квартир с fregat.py\n")
    return db


parse_flats()
