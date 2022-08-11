import os
import shutil
import datetime

from pymongo import MongoClient
from django.core.files.uploadedfile import UploadedFile
from django.db.utils import IntegrityError

from property.models import Flats, Property


def run():
    client = MongoClient('127.0.0.1', 27017)
    db = client['flats_vl']
    items = db.flats.find({})
    fl_objects = Flats.objects.filter(fl_status='free')
    fl_objects.delete()
    current_dir = os.getcwd()
    path_to_dir = os.path.join(current_dir, 'media/flats/')
    try:
        shutil.rmtree(path_to_dir)
    except FileNotFoundError:
        pass
    for el in items:
        try:
            if el['num_fl'] != '':
                pr = Property.objects.get(name=el['living_complex_name'])
                fl = Flats(
                    pk=el['_id'],
                    fk_object=pr,
                    build_num=el['num_dom'],
                    fl_type=el['flat_type'],
                    fl_num=el['num_fl'],
                    floor=el['floor'],
                    fl_decor=el['flat_decor'],
                    fl_price=el['price'],
                    fl_sq=el['flat_sq'],
                )
                fl.fl_drawing.save(el['path_to_planning'].split('/')[-1], UploadedFile(file=open(el['path_to_planning'], 'rb'), content_type='image/png'))
            elif el['num_fl'] == '' and el['path_to_planning'] == '':
                pr = Property.objects.get(name=el['living_complex_name'])
                fl = Flats(
                    pk=el['_id'],
                    fk_object=pr,
                    build_num=el['num_dom'],
                    fl_type=el['flat_type'],
                    floor=el['floor'],
                    fl_decor=el['flat_decor'],
                    fl_price=el['price'],
                    fl_sq=el['flat_sq'],
                )
                fl.save()
            else:
                pr = Property.objects.get(name=el['living_complex_name'])
                fl = Flats(
                    pk=el['_id'],
                    fk_object=pr,
                    build_num=el['num_dom'],
                    fl_type=el['flat_type'],
                    floor=el['floor'],
                    fl_decor=el['flat_decor'],
                    fl_price=el['price'],
                    fl_sq=el['flat_sq'],
                )
                fl.fl_drawing.save(el['path_to_planning'].split('/')[-1],
                                   UploadedFile(file=open(el['path_to_planning'], 'rb'), content_type='image/png'))
        except IntegrityError:
            pass
    with open(os.path.join(os.path.dirname(__file__), 'log_db.txt'), 'a') as f:
        f.write(f"OK *** {datetime.datetime.now().strftime('%d.%m%y %H:%M')} *** added to postgres db successfully\n")
