import time
import requests
import re
import datetime
import os
import math

from PIL import Image
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pdf_compressor.ilovepdf import Compress

from pprint import pprint


OBJS_ID = []


def authentication():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # param = {'grant_type': 'client_credentials',
    #          'client_id': 'app-ext-bashni.1202500029115.eisgs',
    #          'client_secret': '4497c104-45d0-48e9-8884-92d963d12bd5'}
    param = {
        'grant_type': 'client_credentials',
        'client_id': 'app-ext-bashni.1202500029115.eisgs',
        'client_secret': 'ac3656d5-afda-4a9b-8d31-27018f8e8789'
    }
    # req = requests.post(
    #     'https://int.domrf.ru/idm-services/auth/realms/external-eisgs-idm/protocol/openid-connect/token',
    #     headers=headers, data=param)
    req = requests.post(
        'https://наш.дом.рф/idm-services/auth/realms/external-eisgs-idm/protocol/openid-connect/token',
        headers=headers, data=param
    )
    r = req.json()
    hed = {'Authorization': f'Bearer {r["access_token"]}',
           'Content-Type': 'application/json; charset=UTF-8'}
    return hed


def parse_info():
    months = {
        '01': 'Январь',
        '02': 'Февраль',
        '03': 'Март',
        '04': 'Апрель',
        '05': 'Май',
        '06': 'Июнь',
        '07': 'Июль',
        '08': 'Август',
        '09': 'Сентябрь',
        '10': 'Октябрь',
        '11': 'Ноябрь',
        '12': 'Декабрь'
    }
    client = MongoClient('127.0.0.1', 27017)
    db = client['nashdom_vl_db']
    main_collection = db['main']
    count = 0
    hed = authentication()
    url = 'https://наш.дом.рф/gw/sgs/api/v2/construction-objects?address=Владивосток&page=0&size=50'
    req = requests.get(url, headers=hed)
    time.sleep(5)
    pages = 1
    if req.status_code == 200:
        count += 1
        res = req.json()
        pages = math.ceil(res['total'] / res['limitItems'])
    for page in range(pages):
        hed = authentication()
        url = f'https://наш.дом.рф/gw/sgs/api/v2/construction-objects?address=Владивосток&page={page}&size=50'
        time.sleep(5)
        req = requests.get(url, headers=hed)
        if req.status_code == 200:
            res = req.json()
            elements = res['elements']['constructionObjectShortInfo']
            for el in range(len(elements)):
                db_item = {}
                try:
                    if elements[el]['address']['address']['localityName'] == 'Владивосток':
                        print(elements[el]['objectId'])
                        if elements[el]["livingArea"] != 0.0:
                            dom_id = int(str(elements[el]['objectId']).replace('-', '').strip())
                            # if main_collection.count_documents({'_id': db_item['_id']}) == 0:
                            db_item['_id'] = dom_id
                            db_item['object_status'] = elements[el]['objectStatus']['name']
                            if db_item['object_status'] == 'Строится':
                                OBJS_ID.append(dom_id)
                            try:
                                name = elements[el]['titleName']
                                reg_exp = r'ЖК|Жилой комплекс|Жилой комплекс\w|Жилой Комплекс|ЖИЛОЙ КОМПЛЕКС'
                                if re.match(reg_exp, name):
                                    db_item['name'] = re.split(reg_exp, name)[1].strip().replace('"', '').replace('«', '').replace('»', '').capitalize()
                                else:
                                    db_item['name'] = name
                            except Exception:
                                db_item['name'] = 'Не указан'
                            addr = elements[el]['address']['addressString']
                            db_item['address'] = addr
                            try:
                                db_item['district'] = elements[el]['address']['address']['district']
                            except Exception:
                                db_item['district'] = 'р-н не указан'

                            try:
                                num_dom = elements[el]['address']['address']['house']
                                db_item['dom_name'] = f'д. {num_dom}'
                            except KeyError:
                                reg_exp = r"дом|строение|д.\d+|д.\s\d+"
                                if re.search(reg_exp, addr):
                                    db_item['dom_name'] = "".join(addr.partition(re.search(reg_exp, addr).group(0))[-2:])
                                else:
                                    if re.search(r'д.\d+|д.\s\d+|строение|корпус|литера', addr):
                                        db_item['dom_name'] = "".join(addr.partition(re.search(r'д.\d+|д.\s\d+|строение|корпус|литера', addr).group(0))[-2:])
                                    else:
                                        db_item['dom_name'] = ''
                            db_item['flats'] = elements[el]['apartmentsCount']
                            db_item['pr_declaration'] = f'№{elements[el]["projectDeclaration"]["number"]} от {elements[el]["projectDeclaration"]["publishDate"]}'
                            dev_id = elements[el]['developerId']
                            # developer = requests.get(f'https://int.domrf.ru/gw/sgs/api/v2/developers/{dev_id}', headers=hed)
                            developer = requests.get(f'https://наш.дом.рф/gw/sgs/api/v2/developers/{dev_id}', headers=hed)
                            time.sleep(5)
                            if developer.status_code == 200:
                                count += 1
                                resp = developer.json()
                                if resp['nameInfo']['legalForm']['code'] == '4':
                                    db_item['owner'] = f"ООО {resp['nameInfo']['shortName']}"
                                else:
                                    db_item['owner'] = resp['nameInfo']['shortName']
                            # r = requests.get(f'https://int.domrf.ru/gw/sgs/api/v2/construction-objects/{elements[el]["objectId"]}/extended', headers=hed)
                            hed = authentication()
                            r = requests.get(f'https://наш.дом.рф/gw/sgs/api/v2/construction-objects/{elements[el]["objectId"]}/extended', headers=hed)
                            time.sleep(5)
                            if r.status_code == 200:
                                count += 1
                                resp = r.json()
                                db_item['storeys'] = ''
                                db_item['living_sq'] = resp['livingArea']
                                db_item['main_class'] = resp['propertyClass']['name']
                                db_item['wall_decor'] = resp['decoration']['name']
                                db_item['all_material'] = resp['floorMaterial']['name']
                                if resp['isFreePlan'] == False:
                                    db_item['planning'] = 'Нет'
                                else:
                                    db_item['planning'] = 'Есть'
                                try:
                                    db_item['term_keys'] = datetime.datetime.strptime(resp['commissioningPlanDate'], "%Y-%m-%d")
                                except Exception:
                                    db_item['term_keys'] = '-'
                                db_item['building_term'] = ''
                                db_item['ceil_height'] = ''
                                try:
                                    db_item['mid_price'] = resp['objectPriceAVG']
                                except Exception:
                                    db_item['mid_price'] = '-'
                                db_item['builder'] = ''
                                path_to_media = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/property/test')
                                if not os.path.isdir(f'{path_to_media}/{str(dom_id)}/'):
                                    try:
                                        img_list = []
                                        main_imgs = resp['objectsRenders']['objectRender']
                                        path_to_media = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/property/test')

                                        os.makedirs(f'{path_to_media}/{str(dom_id)}/', exist_ok=True)
                                        for img in range(len(main_imgs)):
                                            if img > 5:
                                                break
                                            filename = f'{path_to_media}/{str(dom_id)}/{main_imgs[img]["fileInfo"]["name"][-20:]}'
                                            img_list.append(filename)
                                            if not os.path.exists(filename):
                                                url_file = requests.get(
                                                    f'https://наш.дом.рф/gw/sgs/api/v2/construction-objects/{elements[el]["objectId"]}/files/{main_imgs[img]["fileInfo"]["fileId"]}', headers=hed)
                                                if url_file.status_code == 200:
                                                    count += 1
                                                    time.sleep(5)
                                                    with open(filename, 'wb') as f:
                                                        f.write(url_file.content)
                                                try:
                                                    org_img = Image.open(filename)
                                                    width, height = org_img.size
                                                    if width > 640:
                                                        width_ratio = round(640 / width * 100)
                                                        if org_img.mode == 'RGBA' or org_img.mode == 'P':
                                                            org_img = org_img.convert('RGB')
                                                        org_img.save(filename, quality=width_ratio)
                                                except Exception:
                                                    pass
                                                if img == 0:
                                                    img_1 = Image.open(filename)
                                                    width, height = img_1.size
                                                    if width > 240:
                                                        width_ratio = round(240 / width * 100)
                                                        if img_1.mode == 'RGBA' or img_1.mode == 'P':
                                                            img_1 = img_1.convert('RGB')
                                                        new_img = f"{filename.split('.')[0]}_small.jpg"
                                                        img_1.save(os.path.join(f'{path_to_media}/{str(dom_id)}', new_img), quality=width_ratio)
                                                        db_item['small_img'] = os.path.join(f'{path_to_media}/{str(dom_id)}', new_img)
                                        db_item['main_photos'] = img_list
                                    except Exception:
                                        db_item['main_photos'] = []
                                        db_item['small_img'] = ''
                                else:
                                    db_item['main_photos'] = []
                                    db_item['small_img'] = ''
                            hed = authentication()
                            doc = requests.get(f'https://наш.дом.рф/gw/sgs/api/v2/construction-objects/{elements[el]["objectId"]}/documents', headers=hed)
                            time.sleep(5)
                            if doc.status_code == 200:
                                count += 1
                                doc = doc.json()
                                pages = math.ceil(doc['total'] / doc['limitItems'])
                                doc_list = []
                                doc_dict = {}
                                for page in range(pages):
                                    doc = requests.get(f'https://наш.дом.рф/gw/sgs/api/v2/construction-objects/{elements[el]["objectId"]}/documents?page={page}', headers=hed)
                                    time.sleep(5)
                                    if doc.status_code == 200:
                                        count += 1
                                        doc = doc.json()
                                        for item in range(len(doc['elements']['documentInfo'])):
                                            if item == 0 and doc['elements']['documentInfo'][0]['form']['code'] == 'Ф-ПД' and doc['elements']['documentInfo'][0]['publishDate'] == elements[el]["projectDeclaration"]["publishDate"]:
                                                db_item['pr_decl_link'] = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/api/ext/file/{doc["elements"]["documentInfo"][0]["files"]["fileInfo"][0]["fileId"]}?filename=obj{elements[el]["objectId"]}-pd-{elements[el]["projectDeclaration"]["number"]}.pdf'
                                            elif doc['elements']['documentInfo'][item]['form']['code'] == 'Ф-ПД':
                                                continue
                                            elif doc['elements']['documentInfo'][item]['form']['code'] != 'Ф-ПД':
                                                if doc['elements']['documentInfo'][item]['files'] and doc['elements']['documentInfo'][item]['status']['name'] == 'Размещен':
                                                    if doc['elements']['documentInfo'][item]['files']['fileInfo'][0]['extension'] == 'PDF':
                                                        el_dict = {}

                                                        if doc['elements']['documentInfo'][item]['form']['name'] in doc_dict.values():
                                                            continue
                                                        else:
                                                            doc_dict[f'doc_name_{page}_{item}'] = doc['elements']['documentInfo'][item]['form']['name']
                                                            el_dict['name'] = doc['elements']['documentInfo'][item]['form']['name']
                                                            el_date = doc['elements']['documentInfo'][item]['files']['fileInfo'][0]['uploadDate']
                                                            if re.match(r'Извещение о начале строительства', el_dict['name']):
                                                                db_item['start_date'] = datetime.datetime.strptime(el_date, "%Y-%m-%d")
                                                            el_dict['date'] = datetime.datetime.strptime(el_date, "%Y-%m-%d")
                                                            path_to_media = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/property/test')
                                                            os.makedirs(f'{path_to_media}/{str(dom_id)}/documents', exist_ok=True)
                                                            filename = f'{path_to_media}/{str(dom_id)}/documents/{el_dict["name"]}.pdf'
                                                            el_dict['link'] = filename
                                                            file_id = doc['elements']['documentInfo'][item]['files']['fileInfo'][0]['fileId']
                                                            doc_list.append(el_dict)
                                                            if not os.path.exists(filename):
                                                                url_file = requests.get(f'https://наш.дом.рф/gw/sgs/api/v2/construction-objects/{elements[el]["objectId"]}/files/{file_id}', headers=hed)
                                                                time.sleep(5)
                                                                if url_file.status_code == 200:
                                                                    count += 1
                                                                    with open(filename, 'wb') as f:
                                                                        f.write(url_file.content)
                                                                        # if os.path.getsize(filename) > 1500000:
                                                                        #     try:
                                                                        #         compress = Compress(public_key='project_public_70b6e45cbb17156671e50b60569bc4bf_uK-k-754783948ba558dfa56c054706e44ac5')
                                                                        #         compress.add_file(filename)
                                                                        #         compress.download()
                                                                        #         compress.delete_current_task()
                                                                        #     except Exception as e:
                                                                        #         print(e)
                                                                        #         pass
                                db_item['documents'] = doc_list
                            hed = authentication()
                            m = requests.get(f'https://наш.дом.рф/gw/sgs/api/v2/construction-objects/{elements[el]["objectId"]}/photos', headers=hed)
                            time.sleep(5)
                            # path_to_media = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/property/строится')
                            path_to_media = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/property/test')
                            if m.status_code == 200:
                                # count += 1
                                res = m.json()
                                pages = math.ceil(res['total'] / res['limitItems'])
                                d_img = {}
                                imgs_year_22 = 0
                                for page in range(pages):
                                    if imgs_year_22 == 1:
                                        db_item['build_imgs'] = d_img
                                        break
                                    hed = authentication()
                                    m = requests.get(f'https://наш.дом.рф/gw/sgs/api/v2/construction-objects/{elements[el]["objectId"]}/photos?page={page}&size=10', headers=hed)
                                    time.sleep(5)
                                    if m.status_code == 200:
                                        print('photo page= ', page)
                                        count += 1
                                        res = m.json()
                                        try:
                                            imgs = res['elements']['objectPhoto']
                                            for img in range(len(imgs)):
                                                k_month = imgs[img]['periodDate'].split('-')[1]
                                                year = imgs[img]['periodDate'].split('-')[0]
                                                if db_item['object_status'] == 'Строится' and int(imgs[img]['periodDate'].split('-')[0]) != datetime.date.today().year:
                                                    continue
                                                if os.path.isdir(f'{path_to_media}/{str(dom_id)}/building/{months[k_month]}, {year}') and len(d_img[f'{months[k_month]}, {year}']) > 3:
                                                    continue
                                                os.makedirs(f'{path_to_media}/{str(dom_id)}/building/{months[k_month]}, {year}', exist_ok=True)
                                                filename = f'{path_to_media}/{str(dom_id)}/building/{months[k_month]}, {year}/{imgs[img]["fileInfo"]["name"][-20:]}'
                                                try:
                                                    if len(d_img.keys()) > 6:
                                                        break
                                                    d_img[f'{months[k_month]}, {year}']
                                                except KeyError:
                                                    if db_item['object_status'] == 'Строится':
                                                        d_img[f'{months[k_month]}, {year}'] = []
                                                    elif db_item['object_status'] == 'Сдан':
                                                        if not d_img:
                                                            d_img[f'{months[k_month]}, {year}'] = []
                                                        else:
                                                            imgs_year_22 = 1
                                                            break
                                                if len(d_img[f'{months[k_month]}, {year}']) < 3:
                                                    d_img[f'{months[k_month]}, {year}'].append(filename)
                                                    if not os.path.exists(filename):
                                                        url_file = requests.get(f'https://наш.дом.рф/gw/sgs/api/v2/construction-objects/{elements[el]["objectId"]}/files/{imgs[img]["fileInfo"]["fileId"]}', headers=hed)
                                                        if url_file.status_code == 200:
                                                            count += 1
                                                            time.sleep(5)
                                                            with open(filename, 'wb') as f:
                                                                f.write(url_file.content)
                                                        try:
                                                            org_img = Image.open(filename)
                                                            width, height = org_img.size
                                                            if width > 640:
                                                                width_ratio = round(640 / width * 100)
                                                                if org_img.mode == 'RGBA' or org_img.mode == 'P':
                                                                    org_img = org_img.convert('RGB')
                                                                org_img.save(filename, quality=width_ratio)
                                                        except Exception:
                                                            pass
                                                else:
                                                    continue
                                                # if imgs[img]['periodDate'].split('-')[0] == '2022':
                                                #
                                                # else:
                                                #     if page > 5:
                                                #         imgs_year_22 = 1
                                                #         break
                                        except KeyError:
                                            db_item['build_imgs'] = {}
                                    else:
                                        print('staus code =', m.status_code)
                                db_item['build_imgs'] = d_img
                    else:
                        continue
                except KeyError as e:
                    print(e)
                    print(db_item)
                    continue
                pprint(db_item)
                print('---------------')
                # if el > 2:
                #     print()


                    #
                    # else:
                    #     pass
    print('script done')


parse_info()
