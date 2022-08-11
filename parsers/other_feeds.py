from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from xml.dom import minidom
from urllib.request import Request, urlopen
import requests
import os
import re
import datetime
from pprint import pprint


def parse_feeds():
    client = MongoClient('127.0.0.1', 27017)
    db = client['flats_vl']
    db.flats.delete_many({'living_complex_name': 'More'})
    db.flats.delete_many({'living_complex_name': 'Premium park'}) 
    urls = [
        'https://domoplaner.ru/dc-api/feeds/147-LQ35dsekQPEVoYjzKTPo49NUDQ9ZVxbkRFFBIZmHoWHPoLoWBPrIvnV9OOQ9RlmR/',
        'https://domoplaner.ru/dc-api/feeds/147-TuHzuUY83xwRTxNerSZmmj7xuEH2P6hzqnf8ZLDYwWUvArNXL6jKZ63oKHJ0l4Iy/'
    ]
    for url in range(len(urls)):
        print(urls[url])
        # webFile = urllib.request.urlopen(urls[url], headers={"User-Agent": "Mozila/5.0"})
        # data = web_file.read()
        web_file = Request(urls[url], headers={"User-Agent": "Mozila/5.0"})
        data = urlopen(web_file).read()
        dom = minidom.parseString(data)
        dom.normalize()
        flats = dom.getElementsByTagName('offer')
        counter_0 = 97000
        counter_1 = 98000
        for flat in flats:
            db_item = {}
            for item in flat.childNodes:
                if item.nodeType == 1:
                    if url == 0:
                        db_item['living_complex_name'] = 'More'
                        db_item['_id'] = int(counter_0 + 1)
                        counter_0 += 1
                    else:
                        db_item['living_complex_name'] = 'Premium park'
                        db_item['_id'] = int(counter_1 + 1)
                        counter_1 += 1
                    db_item['floor'] = 1
                    db_item['num_fl'] = ''
                    db_item['flat_decor'] = 'whitebox'
                    if item.tagName == 'categoryId':
                        db_item['num_dom'] = int(item.firstChild.data)
                    if item.tagName == 'price':
                        db_item['price'] = int(item.firstChild.data)
                    if item.tagName == 'name':
                        db_item['flat_sq'] = float(item.firstChild.data.split()[1])
                        if item.firstChild.data.split()[0] == 'Однокомнатная':
                            db_item['flat_type'] = '1'
                        elif item.firstChild.data.split()[0] == 'Двухкомнатная':
                            db_item['flat_type'] = '2'
                        elif item.firstChild.data.split()[0] == 'Трехкомнатная':
                            db_item['flat_type'] = '3'
                    if item.tagName == 'picture':
                        plan_url = item.firstChild.data.strip()
                        db_item['planning_url'] = plan_url
                        path_to_media = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/flats')
                        os.makedirs(f'{path_to_media}/{db_item["living_complex_name"]}', exist_ok=True)
                        filename = f'{path_to_media}/{db_item["living_complex_name"]}/{plan_url.split("/")[-1].split("?")[0]}'
                        db_item['path_to_planning'] = filename
                        if not os.path.exists(filename):
                            if re.match('https', plan_url):
                                r = requests.get(plan_url)
                            else:
                                 r = requests.get(f'https:{plan_url}')
                            with open(filename, 'wb') as f:
                                f.write(r.content)               
            # pprint(db_item)
            # print('----------------------------')     
            try:
                db.flats.insert_one(db_item)
            except DuplicateKeyError:
                print(db.flats.find_one({'_id': db_item['_id']}))
                print('-------------------------')
                                                  
    logger_path = os.path.join(os.path.dirname(__file__), 'flats_logger.txt')
    with open(logger_path, 'a') as f:
        f.write(f"OK *** {datetime.datetime.now().strftime('%d.%m.%y %H:%M')} *** успешно спарсены  квартиры с feeds.py\n")
    print('script done')
    return db


parse_feeds()
