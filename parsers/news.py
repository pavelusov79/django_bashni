import re
import os
import requests
import datetime

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from lxml import html


def parse_links():
    url_links = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    for i in range(1, 20):
        url = f'https://111bashni.ru/novosti/page/{i}'
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            dom = html.fromstring(res.text)
            links = dom.xpath('//h2[@class="entry-title"]/a/@href')
            for link in links:
                url_links.append(link)
    return url_links


def parse_news():
    client = MongoClient('127.0.0.1', 27017)
    db = client['bashni_news']
    collection = db.main
    urls = parse_links()
    # urls = ['https://111bashni.ru/novosti/%d0%ba%d0%b0%d0%ba-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d1%8b-%d0%b2%d0%bb%d0%b0%d0%b4%d0%b8%d0%b2%d0%be%d1%81%d1%82%d0%be%d0%ba%d0%b0-%d1%81%d1%82%d0%b0%d0%bd%d0%be%d0%b2%d1%8f%d1%82%d1%81%d1%8f-%d0%bf']
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    for url in urls:
        res = requests.get(url, headers=header)
        if res.status_code == 200:
            db_item = {}
            dom = html.fromstring(res.text)
            db_item['url'] = url
            p_date = dom.xpath('//p[contains(@class, "entry-meta-time")]/text()')[0]
            db_item['date'] = datetime.datetime.strptime(p_date, "%d.%m.%Y")
            db_item['_id'] = int(p_date.replace('.', ''))
            if db.main.count_documents({'_id': db_item['_id']}) == 0:
                title = dom.xpath('//h1/a/text()')[0]
                db_item['title'] = title
                text = dom.xpath('//div[@class="entry-content"]//*[preceding-sibling::p[@class="entry-meta entry-meta-time"]]//text()')
                clear_text = [item for item in text if not re.search('\n', item) or not re.search(r'\r', item)]
                db_item['text'] = " ".join(clear_text)
                db_item['tags'] = dom.xpath('//p[contains(@class, "entry-meta-tags")]/a/text()')
                db_item['img'] = dom.xpath('//figure[@class="entry-image"]/a/img/@data-src')[0]
                path_to_media = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/news')
                os.makedirs(f'{path_to_media}', exist_ok=True)
                filename = f'{path_to_media}/{db_item["img"].split("/")[-1]}'
                db_item['path_to_img'] = filename
                if not os.path.exists(filename):
                    try:
                        r = requests.get(db_item['img'])
                        with open(filename, 'wb') as f:
                            f.write(r.content)
                    except Exception:
                        db_item['path_to_img'] = ''
                try:
                    collection.insert_one(db_item)
                except DuplicateKeyError:
                    pass
    print('script was done successfully')
            

parse_news()

