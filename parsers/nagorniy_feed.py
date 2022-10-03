from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from xml.dom import minidom
from urllib.request import Request, urlopen
import requests
import os
import re
import datetime
from pprint import pprint


def parse_feed():
    client = MongoClient('127.0.0.1', 27017)
    db = client['flats_vl']
    urls = [
       'https://pb14033.profitbase.ru/export/profitbase_xml/56f718ac5a334037abdae769e23d8877?scheme=https'
    ]
    for url in urls:
        # webFile = urllib.request.urlopen(urls[url], headers={"User-Agent": "Mozila/5.0"})
        # data = web_file.read()
        web_file = Request(url, headers={"User-Agent": "Mozila/5.0"})
        data = urlopen(web_file).read()
        dom = minidom.parseString(data)
        dom.normalize()
        db.flats.delete_many({'living_complex_name': 'Нагорный'})
        flats = dom.getElementsByTagName('offer')
        for flat in flats:
            db_item = {}
            db_item['flat_decor'] = 'Нет'
            db_item['living_complex_name'] = 'Нагорный'
            db_item['num_dom'] = 6
            db_item['_id'] = int(flat._attrs['internal-id'].value)
            for item in flat.childNodes:
                if item.nodeType != 3 and item.tagName == 'status':
                    db_item['status'] = item.firstChild.data
                if item.nodeType != 3 and item.tagName == 'price':
                    if item.firstChild.firstChild.data == '0':
                        db_item['price'] = '-'
                    else:
                        db_item['price'] = int(item.firstChild.firstChild.data)
                if item.nodeType != 3 and item.tagName == 'area':
                    db_item['flat_sq'] = float(item.firstChild.firstChild.data)
                if item.nodeType != 3 and item.tagName == 'number':
                    db_item['num_fl'] = int(item.firstChild.data)
                if item.nodeType != 3 and item.tagName == 'floor':
                    db_item['floor'] = int(item.firstChild.data)
                if item.nodeType != 3 and item.tagName == 'rooms':
                    if item.firstChild.data == '0':
                        db_item['flat_type'] = 'C'
                    else:
                        db_item['flat_type'] = item.firstChild.data
                if item.nodeType != 3 and item.tagName == 'image' and item._attrs['type'].value == 'plan':
                    plan_url = item.firstChild.data.strip()
                    db_item['planning_url'] = plan_url
                    path_to_media = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/flats')
                    os.makedirs(f'{path_to_media}/{db_item["living_complex_name"]}', exist_ok=True)
                    filename = f'{path_to_media}/{db_item["living_complex_name"]}/{plan_url.split("/")[-1].split("?")[0][-7:]}'
                    db_item['path_to_planning'] = filename
                    if not os.path.exists(filename):
                        if re.match('https', plan_url):
                            r = requests.get(plan_url)
                        else:
                            r = requests.get(f'https:{plan_url}')
                        with open(filename, 'wb') as f:
                            f.write(r.content)
            # if db_item['status'] == 'AVAILABLE' and db_item['floor'] > 0:
            #     pprint(db_item)
            #     print('-----------------------------')
            try:
                if db_item['status'] == 'AVAILABLE' and db_item['floor'] > 0:
                    db.flats.insert_one(db_item)
            except DuplicateKeyError:
                print('duplicate found')
                print(db.flats.find_one({'_id': db_item['_id']}))
                try:
                    db_item['_id'] = int(f'9{db_item["_id"]}')
                    db.flats.insert_one(db_item)
                except DuplicateKeyError:
                    print('duplicate 2!')

    logger_path = os.path.join(os.path.dirname(__file__), 'flats_logger.txt')
    with open(logger_path, 'a') as f:
        f.write(f"OK *** {datetime.datetime.now().strftime('%d.%m.%y %H:%M')} *** успешно спарсено {db.flats.count_documents({'living_complex_name': 'Нагорный'})} квартир с nagorniy_feed.py\n")
    print('script done')
    return db


parse_feed()
