import os
import shutil
from pymongo import MongoClient

from property.models import BuildingObjects, BuildingPhotos, ObjectDocuments, CheckObjectReadiness, \
    CheckTermsPassKeys, MainPhotos, City, BuildMonths
from django.core.files.uploadedfile import UploadedFile


def run():
    client = MongoClient('127.0.0.1', 27017)
    db = client['nashdom_vl_db']
    items = db.main_collection.find({})
    # build_objs = BuildingObjects.objects.filter(build_stage='b')
    # build_objs.delete()
    # current_dir = os.getcwd()
    # path_to_dir = os.path.join(current_dir, 'media/property/строится')
    # try:
    #     shutil.rmtree(path_to_dir)
    # except FileNotFoundError:
    #     pass
    city = City.objects.get(city_name='Владивосток')
    for el in items:
        if not BuildingObjects.objects.filter(id=el['_id']):
            print(el['_id'])
            path_to_dir = os.path.join(os.getcwd(), f'media/property/строится/{el["_id"]}')
            try:
                shutil.rmtree(path_to_dir)
            except FileNotFoundError:
                pass
            if el['term_keys'] == '-' and el['mid_price'] == '-':
                obj = BuildingObjects(
                    id=el['_id'],
                    name=el['name'],
                    addr=el['address'],
                    main_contractor=el['main_contractor'],
                    building_company=el['builder'],
                    pr_declaration=el['pr_declaration'],
                    pr_decl_link=el['pr_decl_link'],
                    operation_term=el['building_term'],
                    property_class=el['main_class'],
                    wall=el['all_material'],
                    decoration=el['wall_decor'],
                    free_planning=el['planning'],
                    floors=el['storeys'],
                    q_flats=el['flats'],
                    living_sq=el['living_sq'],
                    ceil_height=el['ceil_height'],
                    city=city
                )
                obj.small_img.save(el['small_img'].split('/')[-1], UploadedFile(file=open(el['small_img'], 'rb'), content_type='image/jpg'))
            elif el['mid_price'] == '-':
                obj = BuildingObjects(
                    id=el['_id'],
                    name=el['name'],
                    addr=el['address'],
                    main_contractor=el['main_contractor'],
                    building_company=el['builder'],
                    pr_declaration=el['pr_declaration'],
                    pr_decl_link=el['pr_decl_link'],
                    operation_term=el['building_term'],
                    property_class=el['main_class'],
                    wall=el['all_material'],
                    decoration=el['wall_decor'],
                    free_planning=el['planning'],
                    floors=el['storeys'],
                    q_flats=el['flats'],
                    living_sq=el['living_sq'],
                    ceil_height=el['ceil_height'],
                    city=city,
                    send_keys=el['term_keys']
                )
                obj.small_img.save(el['small_img'].split('/')[-1],
                                   UploadedFile(file=open(el['small_img'], 'rb'), content_type='image/jpg'))
            else:
                obj = BuildingObjects(
                    id=el['_id'],
                    name=el['name'],
                    addr=el['address'],
                    main_contractor=el['main_contractor'],
                    building_company=el['builder'],
                    pr_declaration=el['pr_declaration'],
                    pr_decl_link=el['pr_decl_link'],
                    operation_term=el['building_term'],
                    property_class=el['main_class'],
                    wall=el['all_material'],
                    decoration=el['wall_decor'],
                    free_planning=el['planning'],
                    floors=el['storeys'],
                    q_flats=el['flats'],
                    living_sq=el['living_sq'],
                    ceil_height=el['ceil_height'],
                    city=city,
                    send_keys=el['term_keys'],
                    middle_price=el['mid_price']
                )
                obj.small_img.save(el['small_img'].split('/')[-1],
                                   UploadedFile(file=open(el['small_img'], 'rb'), content_type='image/jpg'))

            main_photos = el['main_photos']
            for item in main_photos:
                ph = MainPhotos(fk_property=obj)
                ph.main_img.save(item.split('/')[-1], UploadedFile(file=open(item, 'rb'), content_type='image/jpg'))

            build_photos = el['build_imgs']
            if build_photos:
                for k, items in build_photos.items():
                    m = BuildMonths(fk_property=obj, build_month=k)
                    m.save()
                    for i in items:
                        b_ph = BuildingPhotos(fk_month=m)
                        b_ph.build_img.save(i.split('/')[-1], UploadedFile(file=open(i, 'rb'), content_type='image/jpg'))

            docs = el['documents']
            if docs:
                for doc in docs:
                    d = ObjectDocuments(fk_object=obj, doc_name=doc['name'], doc_date=doc['date'], doc_link=doc['link'])
                    d.save()

            delay_terms = el['delay_terms']
            for term in delay_terms:
                if term.split()[1] == '-':
                    d_t = CheckObjectReadiness(fk_object=obj,
                                               readiness=term.split()[0],
                                               initial_date=' '.join(term.split()[1]),
                                               changed_date=' '.join(term.split()[2:5]),
                                               note=' '.join(term.split()[5:]))
                    d_t.save()
                elif term.split()[1] == '-' and term.split()[2] == '-':
                    d_t = CheckObjectReadiness(fk_object=obj,
                                               readiness=term.split()[0],
                                               initial_date=' '.join(term.split()[1]),
                                               changed_date=' '.join(term.split()[2]),
                                               note=' '.join(term.split()[3:]))
                    d_t.save()
                else:
                    d_t = CheckObjectReadiness(fk_object=obj,
                                               readiness=term.split()[0],
                                               initial_date=' '.join(term.split()[1:4]),
                                               changed_date=' '.join(term.split()[4:7]),
                                               note=' '.join(term.split()[7:]))
                    d_t.save()

            delay_keys = el['delay_keys']
            if delay_keys[2] != '':
                k = CheckTermsPassKeys(fk_object=obj, initial_date=delay_keys[0], changed_date=delay_keys[1],
                                       note=delay_keys[2])
                k.save()
            else:
                k = CheckTermsPassKeys(fk_object=obj, initial_date=delay_keys[0], changed_date=delay_keys[1])
                k.save()

    buildings = BuildingObjects.objects.filter(city__city_name='Владивосток')
    for build in buildings:
        if db.main.count_documents({'_id': build.id}) == 0:
            build.delete()
            path_to_dir = os.path.join(os.getcwd(), f'media/property/строится/{build.id}')
            try:
                shutil.rmtree(path_to_dir)
            except FileNotFoundError:
                pass