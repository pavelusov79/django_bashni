import requests
from pprint import pprint


def parse_info():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    param = {'grant_type': 'client_credentials',
             'client_id': 'app-ext-bashni.1202500029115.eisgs',
             'client_secret': '4497c104-45d0-48e9-8884-92d963d12bd5'}
    req = requests.post('https://int.domrf.ru/idm-services/auth/realms/external-eisgs-idm/protocol/openid-connect/token', headers=headers, data=param)
    r = req.json()
    print(r['access_token'])
    hed = {'Authorization': f'Bearer {r["access_token"]}',
           'Content-Type': 'application/json; charset=UTF-8'}

    url = 'https://int.domrf.ru/gw/sgs/api/v2/complexes/'
    req = requests.get(url, headers=hed)
    print(req.status_code)
    res = req.json()
    l = res['elements']['complexShortInfo']
    objects_id = []
    for item in l:
        try:
            for i in item['constructionObjects']['constructionObject']:
                objects_id.append(i['objectId'])
        except KeyError:
            continue
    print()


parse_info()
