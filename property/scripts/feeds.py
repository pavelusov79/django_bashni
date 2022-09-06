from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from xml.dom import minidom
from urllib.request import Request, urlopen
import requests
import os
import re
import datetime
from pprint import pprint

from property.models import PropertyFeeds


def run():
    client = MongoClient('127.0.0.1', 27017)
    db = client['flats_vl']
    urls = PropertyFeeds.objects.all()
    # urls = [
        # 'https://s-kvartal.ru/storage/app/uploads/dom_click_feed.xml'
        # 'https://domoplaner.ru/dc-api/feeds/248-2vUKBi8HYGXHOXiPWxlYUN8VON13MrjOICVXUF4msFwx0VW9oPzDYFqyKOs2HKfV/',
        # 'https://api.develug.ru/feed/71/zhk_ayvazovskiy.xml',
    #     'https://api.develug.ru/feed/74/zhk_futurist.xml',
    #     'https://api.develug.ru/feed/72/zhk_kashtanovyy_dvor.xml', 
    #     'https://pb11656.profitbase.ru/export/domclick/6fcad6b30813e28ab0713930ffcb3173',
    #     'https://xn----7sbahwklf6auu3n.xn--p1ai/fid',
    #     'https://domoplaner.ru/dc-api/feeds/13-pW0O6NiYW1GabRrSikIOG00Obcu0uaxg5cOM4Ud8AbCjvKWjXncRSgieKri4lUZg/',
    #     'https://dom.masterstroydv.ru/feed',
    #     'https://pb14188.profitbase.ru/export/domclick/6add6ecc11bbbcabe7d78c7af47537a6',
    #     'https://davinchigrupp.kvartirogramma.ru/feeds/288e18971b8c177c4508769895b3951f.xml'
    # ]
    for url in range(len(urls)):
        print(urls[url].feed)
        # webFile = urllib.request.urlopen(urls[url], headers={"User-Agent": "Mozila/5.0"})
        # data = web_file.read()
        web_file = Request(urls[url].feed, headers={"User-Agent": "Mozila/5.0"})
        data = urlopen(web_file).read()
        dom = minidom.parseString(data)
        dom.normalize()
        flats = dom.getElementsByTagName('flat')
        name = dom.getElementsByTagName('name')
        build_num = dom.getElementsByTagName('id')
        if re.match('ЖК', name[0].firstChild.data):
            if ' '.join(name[0].firstChild.data.split()[1:]).replace('"', '').replace("«", '').replace("»", '') == 'Брусника':
                if build_num[1].firstChild.data == '165603':
                    db.flats.delete_many({'living_complex_name': 'Брусника', 'num_dom': 1})
                elif build_num[1].firstChild.data == '165604':
                    db.flats.delete_many({'living_complex_name': 'Брусника', 'num_dom': 2})
                elif build_num[1].firstChild.data == '165605':
                    db.flats.delete_many({'living_complex_name': 'Брусника', 'num_dom': 3})
                elif build_num[1].firstChild.data == '165606':
                    db.flats.delete_many({'living_complex_name': 'Брусника', 'num_dom': 4})
                elif build_num[1].firstChild.data == '165608':
                    db.flats.delete_many({'living_complex_name': 'Брусника', 'num_dom': 6})
                elif build_num[1].firstChild.data == '165609':
                    db.flats.delete_many({'living_complex_name': 'Брусника', 'num_dom': 7})
            else:
                db.flats.delete_many({'living_complex_name': ' '.join(name[0].firstChild.data.split()[1:]).replace('"', '').replace("«", '').replace("»", '')})
        else:
            db.flats.delete_many({'living_complex_name': name[0].firstChild.data.replace('"', '').replace("«", '').replace("»", '')}) 
        for flat in flats:
            db_item = {}
            for item in flat.childNodes:
                if item.nodeType == 1:
                    if item.tagName == 'flat_id':
                        if re.match('ЖК', name[0].firstChild.data):
                            db_item['living_complex_name'] = ' '.join(name[0].firstChild.data.split()[1:]).replace('"', '').replace("«", '').replace("»", '')
                        else:
                            db_item['living_complex_name'] = name[0].firstChild.data.replace('"', '').replace("«", '').replace("»", '')
                        db_item['_id'] = int(f'{url + 4}{item.firstChild.data}')
                        d = item.parentNode.parentNode.parentNode
                        for el in d.childNodes:
                            if el.nodeType == 1:
                                if el.tagName == 'name':
                                    try:
                                        db_item['num_dom'] = int(el.firstChild.data.split()[-1].replace('№', ''))
                                    except Exception:
                                        if db_item['living_complex_name'] == 'Шилкинский':
                                            db_item['num_dom'] = 8
                                        else:
                                            db_item['num_dom'] = 1
                    if item.tagName == 'floor':
                        db_item['floor'] = int(item.firstChild.data)
                    if item.tagName == 'apartment':
                        db_item['num_fl'] = int(item.firstChild.data)
                    if item.tagName == 'price':
                        try:
                            db_item['price'] = int(item.firstChild.data)
                        except ValueError:
                            db_item['price'] = int(item.firstChild.data.split('.')[0])
                    if item.tagName == 'room':
                        if item.firstChild.data == '0':
                            db_item['flat_type'] = 'C'
                        else:
                            db_item['flat_type'] = item.firstChild.data
                    try:
                        if item.tagName == 'renovation':
                            db_item['flat_decor'] = item.firstChild.data
                    except AttributeError:
                        db_item['flat_decor'] = '-'
                    if item.tagName == 'area':
                        db_item['flat_sq'] = float(item.firstChild.data)
                    if item.tagName == 'plan':
                        plan_url = item.firstChild.data.strip()
                        db_item['planning_url'] = plan_url
                        path_to_media = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'media/flats')
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
            # print('-----------------------------')
            try:
                db.flats.insert_one(db_item)
            except DuplicateKeyError:
                try:
                    db_item['_id'] = f'{db_item["_id"]}{url}'
                    db.flats.insert_one(db_item)
                except DuplicateKeyError:
                    print('found duplicate')

    logger_path = os.path.join(os.path.dirname(__file__), 'flats_logger.txt')
    with open(logger_path, 'a') as f:
        f.write(f"OK *** {datetime.datetime.now().strftime('%d.%m.%y %H:%M')} *** успешно спарсены  квартиры с feeds.py\n")
    print('script done')
    return db


