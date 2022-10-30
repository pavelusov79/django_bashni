from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from slugify import slugify
from PIL import Image

from property.models import Property, City, resize_image


class Tags(models.Model):
    tag_name = models.CharField(max_length=64, verbose_name='тэг')
    slug = models.SlugField(max_length=80, verbose_name='path url')

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name_plural = 'Тэги новостей'
        ordering = ['tag_name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.tag_name, ok='_', only_ascii=True)
        return super(Tags, self).save(*args, **kwargs)


class News(models.Model):
    title = models.CharField(max_length=128, verbose_name="заголовок")
    published = models.DateField(verbose_name="опубликовано", default=datetime.now)
    description = RichTextField(verbose_name="текст новости")
    tags = models.ManyToManyField(Tags, verbose_name='тэги')
    is_active = models.BooleanField(verbose_name='новость активна', default=True)
    likes = models.PositiveSmallIntegerField(verbose_name='лайки', default=0)
    news_visit = models.PositiveSmallIntegerField(verbose_name='просмотры новости', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Новости'
        ordering = ['-published']


class ImageNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='img_news')
    img = models.ImageField(upload_to='news', blank=True, null=True, verbose_name='фото новости', max_length=256)

    def save(self, *args, **kwargs):
        if self.img:
            super().save(*args, **kwargs)
            resize_image(self.img)


class NewsComment(models.Model):
    comment_date = models.DateTimeField(verbose_name='дата комментария', default=datetime.now)
    comment_text = models.TextField(verbose_name='текст комментария')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь комментария')
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='комментарий к новости')
    failed_moderation = models.TextField(verbose_name='комментарий админа портала в случае непрохождения модерации',
                                         blank=True)
    is_active = models.BooleanField(verbose_name='комментарий активен', default=False)

    class Meta:
        verbose_name_plural = 'Комментарии к новостям'


class YoutubeChannel(models.Model):
    name = models.CharField(verbose_name='название видео', max_length=128)
    date = models.DateTimeField(verbose_name='дата', default=datetime.now)
    video_url = models.URLField(max_length=200, verbose_name='ссылка на видео')
    fk_property = models.ForeignKey(Property, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='для ЖК')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Видео youtube'
        ordering = ('-date',)


class Events(models.Model):
    title = models.CharField(max_length=128, verbose_name="заголовок мероприятия")
    start_date = models.DateField(verbose_name="начало мероприятия")
    finish_date = models.DateField(verbose_name="конец мероприятия")
    description = RichTextField(verbose_name="текст мероприятия")
    event_img = models.ImageField(upload_to='events', verbose_name='фото меропритятия', max_length=256)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="город")
    is_active = models.BooleanField(verbose_name='мероприятие активно', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Мероприятия'
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        resize_image(self.event_img)


class SitePolicy(models.Model):
    title = models.CharField(max_length=128, verbose_name="заголовок")
    text = RichTextField(verbose_name="текст")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Политика сайта'


class PersonDataTreatment(models.Model):
    title = models.CharField(max_length=256, verbose_name='заголовок')
    text = RichTextField(verbose_name='текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Обработка персональных данных'



