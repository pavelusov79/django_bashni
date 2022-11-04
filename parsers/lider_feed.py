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
        'https://dom.masterstroydv.ru/feed',
        'https://portal.talan.group/1c/ddu/feeds/clik.xml'
    ]
    for url in range(len(urls)):
        # webFile = urllib.request.urlopen(urls[url], headers={"User-Agent": "Mozila/5.0"})
        # data = web_file.read()
        web_file = Request(urls[url], headers={"User-Agent": "Mozila/5.0"})
        data = urlopen(web_file).read()
        dom = minidom.parseString(data)
        dom.normalize()
        complexes = dom.getElementsByTagName('complex')
        for elem in complexes:
            for el in elem.childNodes:
                if el.nodeType != 3 and el.tagName == 'name':
                    zhk = re.search(r"Лидер|Горизонты", el.firstChild.data)
                    if re.search(r"Лидер|Горизонты", el.firstChild.data):
                        if re.match('ЖК', el.firstChild.data):
                            complex_name = ' '.join(el.firstChild.data.split()[1:]).replace('"', '').replace("«", '').replace("»", '')
                            db.flats.delete_many({'living_complex_name': ' '.join(el.firstChild.data.split()[1:]).replace('"', '').replace("«", '').replace("»", '')})
                        else:
                            complex_name = el.firstChild.data.replace('"', '').replace("«", '').replace("»", '')
                            db.flats.delete_many({'living_complex_name': el.firstChild.data.replace('"', '').replace("«", '').replace("»", '')})
                if el.nodeType != 3 and el.tagName == 'buildings' and zhk:
                    buildings = el.getElementsByTagName('building')
                    for build in buildings:
                        for i in build.childNodes:
                            if i.nodeType != 3 and i.tagName == 'id':
                                dom_id = i.firstChild.data
                            if i.nodeType != 3 and i.tagName == 'name':
                                try:
                                    num_dom = int(i.firstChild.data.split()[-1].replace('№', ''))
                                except Exception:
                                    if complex_name == 'Новые Горизонты' and dom_id == '162704':
                                        num_dom = 1
                                    elif complex_name == 'Новые Горизонты' and dom_id == '165242':
                                        num_dom = 2
                                    else:
                                        num_dom = 1
                            if i.nodeType != 3 and i.tagName == 'flats' and zhk and num_dom:
                                flats = i.getElementsByTagName('flat')
                                for flat in flats:
                                    db_item = {}
                                    db_item['living_complex_name'] = complex_name
                                    db_item['num_dom'] = num_dom
                                    for item in flat.childNodes:
                                        if item.nodeType != 3 and item.tagName == 'flat_id':
                                            db_item['_id'] = int(f'1234{url}{item.firstChild.data}')
                                        if item.nodeType != 3 and item.tagName == 'floor':
                                            db_item['floor'] = int(item.firstChild.data)
                                        if item.nodeType != 3 and item.tagName == 'apartment':
                                            db_item['num_fl'] = int(item.firstChild.data)
                                        if item.nodeType != 3 and item.tagName == 'price':
                                            try:
                                                db_item['price'] = int(item.firstChild.data)
                                            except ValueError:
                                                db_item['price'] = int(item.firstChild.data.split('.')[0])
                                        if item.nodeType != 3 and item.tagName == 'room':
                                            if item.firstChild.data == '0':
                                                db_item['flat_type'] = 'C'
                                            else:
                                                db_item['flat_type'] = item.firstChild.data
                                        try:
                                            if item.nodeType != 3 and item.tagName == 'renovation':
                                                db_item['flat_decor'] = item.firstChild.data
                                        except AttributeError:
                                            db_item['flat_decor'] = '-'
                                        if item.nodeType != 3 and item.tagName == 'area':
                                            db_item['flat_sq'] = float(item.firstChild.data)
                                        if item.nodeType != 3 and item.tagName == 'plan':
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
                                    # if db_item['living_complex_name'] == 'Лидер' and db_item['flat_type'] == '1':
                                    #     pass
                                    # else:
                                    #     pprint(db_item)
                                    #     print('-----------------------------')
                                    if db_item['living_complex_name'] == 'Лидер' and db_item['flat_type'] == '1':
                                        pass
                                    else:
                                        try:
                                            db.flats.insert_one(db_item)
                                        except DuplicateKeyError:
                                            print('duplicate found')
                                            print(db.flats.find_one({'_id': db_item['_id']}))
                                            try:
                                                db_item['_id'] = f'9{db_item["_id"]}'
                                                db.flats.insert_one(db_item)
                                            except DuplicateKeyError:
                                                print('duplicate 2!')

    # logger_path = os.path.join(os.path.dirname(__file__), 'flats_logger.txt')
    # with open(logger_path, 'a') as f:
    #     f.write(f"OK *** {datetime.datetime.now().strftime('%d.%m.%y %H:%M')} *** успешно спарсено {db.flats.count_documents({'living_complex_name': 'Лидер'}) + db.flats.count_documents({'living_complex_name': 'Новые Горизонты'})} квартир с lider_feed.py\n")
    print('script done')
    return db


parse_feed()
