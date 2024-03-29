import os
import shutil
from pymongo import MongoClient
from pathlib import Path

from property.models import BuildingObjects, BuildingPhotos, ObjectDocuments, CheckObjectReadiness, \
    CheckTermsPassKeys, MainPhotos, City, BuildMonths
from django.core.files.uploadedfile import UploadedFile


def run():
    client = MongoClient('127.0.0.1', 27017)
    db = client['nashdom_cities']
    items = db.main.find({})
    for el in items:
        if not BuildingObjects.objects.filter(id=el['_id']):
            print(el['_id'])
            city = City.objects.get(city_name=el['city'])
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
                try:
                    if el['small_img']:
                        # obj.small_img.save(el['small_img'].split('/')[-1], UploadedFile(file=open(el['small_img'], 'rb'), content_type='image/jpg'))
                        obj.small_img = el['small_img'].split('media/')[-1]
                        obj.save()
                    else:
                        file_path = os.path.join(os.getcwd(), 'media/build.jpg')
                        # obj.small_img.save('build.jpg', UploadedFile(file=open(file_path, 'rb'), content_type='image/jpg'))
                        obj.small_img = file_path.split('media/')[-1]
                        obj.save()
                except Exception:
                    file_path = os.path.join(os.getcwd(), 'media/build.jpg')
                    obj.small_img = file_path.split('media/')[-1]
                    obj.save()

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
                try:
                    if el['small_img']:
                        # obj.small_img.save(el['small_img'].split('/')[-1],
                        #                UploadedFile(file=open(el['small_img'], 'rb'), content_type='image/jpg'))
                        obj.small_img = el['small_img'].split('media/')[-1]
                        obj.save()
                    else:
                        file_path = os.path.join(os.getcwd(), 'media/build.jpg')
                        # obj.small_img.save('build.jpg', UploadedFile(file=open(file_path, 'rb'), content_type='image/jpg'))
                        obj.small_img = file_path.split('media/')[-1]
                        obj.save()
                except Exception:
                    file_path = os.path.join(os.getcwd(), 'media/build.jpg')
                    obj.small_img = file_path.split('media/')[-1]
                    obj.save()
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
                try:
                    if el['small_img']:
                        # obj.small_img.save(el['small_img'].split('/')[-1],
                        #                    UploadedFile(file=open(el['small_img'], 'rb'), content_type='image/jpg'))
                        obj.small_img = el['small_img'].split('media/')[-1]
                        obj.save()
                    else:
                        file_path = os.path.join(os.getcwd(), 'media/build.jpg')
                        # obj.small_img.save('build.jpg', UploadedFile(file=open(file_path, 'rb'), content_type='image/jpg'))
                        obj.small_img = file_path.split('media/')[-1]
                        obj.save()
                except Exception:
                    file_path = os.path.join(os.getcwd(), 'media/build.jpg')
                    obj.small_img = file_path.split('media/')[-1]
                    obj.save()

            main_photos = el['main_photos']
            if main_photos:
                for item in main_photos:
                    ph = MainPhotos(fk_property=obj)
                    # ph.main_img.save(item.split('/')[-1], UploadedFile(file=open(item, 'rb'), content_type='image/jpg'))
                    ph.main_img =  item.split('media/')[-1]
                    ph.save()
            else:
                ph = MainPhotos(fk_property=obj)
                file_path = os.path.join(os.getcwd(), 'media/build.jpg')
                # ph.main_img.save('build.jpg', UploadedFile(file=open(file_path, 'rb'), content_type='image/jpg'))
                ph.main_img = file_path.split('media/')[-1]
                ph.save()

            # build_photos = el['build_imgs']
            # if build_photos:
            #     for k, items in build_photos.items():
            #         m = BuildMonths(fk_property=obj, build_month=k)
            #         m.save()
            #         for i in items:
            #             b_ph = BuildingPhotos(fk_month=m)
            #             b_ph.build_img.save(i.split('/')[-1], UploadedFile(file=open(i, 'rb'), content_type='image/jpg'))
            #
            # docs = el['documents']
            # if docs:
            #     for doc in docs:
            #         d = ObjectDocuments(fk_object=obj, doc_name=doc['name'], doc_date=doc['date'], doc_link=doc['link'])
            #         d.save()

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

    buildings = BuildingObjects.objects.filter(city__city_name__in=['Cочи', 'Москва', 'Санкт-Петербург'])
    for build in buildings:
        if db.main.count_documents({'_id': build.id}) == 0:
            build.delete()
            path_to_dir = os.path.join(Path(__file__).parent.parent.parent, f'media/property/строится/{build.id}')
            try:
                shutil.rmtree(path_to_dir)
            except FileNotFoundError:
                pass
