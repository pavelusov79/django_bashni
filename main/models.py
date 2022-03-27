from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField


class Tags(models.Model):
    tag_name = models.CharField(max_length=64, verbose_name='тэг')
    slug = models.SlugField(max_length=80, verbose_name='path url')

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name_plural = 'Тэги новостей'


class News(models.Model):
    title = models.CharField(max_length=64, verbose_name="заголовок")
    published = models.DateField(verbose_name="опубликовано", default=datetime.now)
    description = RichTextField(verbose_name="текст новости")
    tags = models.ManyToManyField(Tags, verbose_name='тэги')
    is_active = models.BooleanField(verbose_name='новость активна', default=True)
    likes = models.PositiveSmallIntegerField(verbose_name='лайки', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Новости'


class ImageNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='img_news')
    img = models.ImageField(upload_to='news', blank=True, verbose_name='фото новости')


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
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Видео youtube'
        ordering = ('-date',)




