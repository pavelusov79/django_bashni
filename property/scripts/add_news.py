from pymongo import MongoClient

from main.models import News, ImageNews, Tags


def run():
    client = MongoClient('127.0.0.1', 27017)
    db = client['bashni_news']
    db_news = News.objects.filter(is_active=True)
    db_news.delete()
    for el in db.main.find({}):
        if el['path_to_img']:
            news_obj = News.objects.create(id=el['_id'], title=el['title'], published=el['date'], description=el['text'])
            for tag_item in el['tags']:
                db_tags = [i[0] for i in Tags.objects.all().values_list('tag_name')]
                if tag_item not in db_tags:
                    Tags.objects.create(tag_name=tag_item)
                    print(tag_item)
                t = Tags.objects.filter(tag_name=tag_item).first()
                news_obj.tags.add(t)
                news_obj.save()

            ImageNews.objects.create(img=el['path_to_img'].split('/media')[-1], news=news_obj)



