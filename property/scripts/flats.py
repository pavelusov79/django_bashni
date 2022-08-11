import os
import datetime

from pymongo import MongoClient
from django.db.utils import IntegrityError

from property.models import Flats, Property, Buildings


def run():
    client = MongoClient('127.0.0.1', 27017)
    db = client['flats_vl']
    items = db.flats.find({})
    fl_objects = Flats.objects.filter(fl_status='free')
    fl_objects.delete()
    for el in items:
        try:
            if el['num_fl'] != '':
                pr = Property.objects.filter(name__icontains=el['living_complex_name']).first()
                fl = Flats(
                    pk=el['_id'],
                    fk_property=pr,
                    fk_building=Buildings.objects.filter(fk_property=pr, num_dom__icontains=el['num_dom']).first(),
                    build_num=el['num_dom'],
                    fl_type=el['flat_type'],
                    fl_num=el['num_fl'],
                    floor=el['floor'],
                    fl_price=el['price'],
                    fl_sq=el['flat_sq'],
                )
                if el['flat_decor'] == 'да' or el['flat_decor'] == 'нет':
                    fl.fl_decor = el['flat_decor'].capitalize()
                else:
                    fl.fl_decor = el['flat_decor']
                # fl.fl_drawing.save(el['path_to_planning'].split('/')[-1], UploadedFile(file=open(el['path_to_planning'], 'rb'), content_type='image/png'))
                fl.fl_drawing = el['path_to_planning'].split('media/')[-1]
                fl.save()
            elif el['num_fl'] == '' and el['path_to_planning'] == '':
                pr = Property.objects.filter(name__icontains=el['living_complex_name']).first()
                fl = Flats(
                    pk=el['_id'],
                    fk_property=pr,
                    fk_building=Buildings.objects.filter(fk_property=pr, num_dom__icontains=el['num_dom']).first(),
                    build_num=el['num_dom'],
                    fl_type=el['flat_type'],
                    floor=el['floor'],
                    fl_price=el['price'],
                    fl_sq=el['flat_sq'],
                )
                if el['flat_decor'] == 'да' or el['flat_decor'] == 'нет':
                    fl.fl_decor = el['flat_decor'].capitalize()
                else:
                    fl.fl_decor = el['flat_decor']
                fl.save()
            else:
                pr = Property.objects.filter(name__icontains=el['living_complex_name']).first()
                fl = Flats(
                    pk=el['_id'],
                    fk_property=pr,
                    fk_building=Buildings.objects.filter(fk_property=pr, num_dom__icontains=el['num_dom']).first(),
                    build_num=el['num_dom'],
                    fl_type=el['flat_type'],
                    floor=el['floor'],
                    fl_price=el['price'],
                    fl_sq=el['flat_sq'],
                )
                if el['flat_decor'] == 'да' or el['flat_decor'] == 'нет':
                    fl.fl_decor=el['flat_decor'].capitalize()
                else:
                    fl.fl_decor=el['flat_decor']
                # fl.fl_drawing.save(el['path_to_planning'].split('/')[-1],
                #                    UploadedFile(file=open(el['path_to_planning'], 'rb'), content_type='image/png'))
                fl.fl_drawing = el['path_to_planning'].split('media/')[-1]
                fl.save()
        except IntegrityError:
            pass
    with open(os.path.join(os.path.dirname(__file__), 'log_db.txt'), 'a') as f:
        f.write(f"OK *** {datetime.datetime.now().strftime('%d.%m%y %H:%M')} *** {db.flats.count_documents({})} added to postgres db successfully\n")
