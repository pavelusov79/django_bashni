from django.db import models
from django.contrib.auth.models import User

from PIL import Image

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from slugify import slugify


def resize_image(elem):
    org_img = Image.open(elem.path)
    width, height = org_img.size
    if width > 900:
        width_ratio = round(900 / width * 100)
        org_img.save(elem.path, quality=width_ratio)


class City(models.Model):
    city_name = models.CharField(verbose_name='город', max_length=32)
    city_slug = models.SlugField(verbose_name='поле url')
    city_code = models.PositiveSmallIntegerField(verbose_name='код города')

    class Meta:
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.city_name


class Facilities(models.Model):
    name = models.CharField(verbose_name='возможности', max_length=128)
    vector = models.TextField(verbose_name='вектор рисунка', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'инфраструктура ЖК'


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField(verbose_name='значение')

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name_plural = 'Звезды рейтинга' 
        ordering = ['-value']


def path_to_property(instance, filename):
    return f'property/{instance.name}/{filename}'


class Property(models.Model):
    STAGE_CHOICES = (
        ('b', 'строится'),
        ('p', 'сдан'),
        ('d', 'долгострой'),
    )
    name = models.CharField(max_length=128, verbose_name='Название ЖК', unique=True)
    slug = models.SlugField(verbose_name='поле url', max_length=128)
    build_stage = models.CharField(max_length=15, verbose_name='Стадия строительства', choices=STAGE_CHOICES, default='b')
    short_desc = RichTextUploadingField(verbose_name='Краткое описание', blank=True)
    territory_desc = RichTextUploadingField(verbose_name='Благоустройство', blank=True)
    infr_desc = RichTextUploadingField(verbose_name='Инфраструктура', blank=True)
    work_desc = RichTextUploadingField(verbose_name='Перечень работ', blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Для города', related_name='prorerty')
    district = models.CharField(verbose_name='район', max_length=64, blank=True)
    buid_video = models.URLField(verbose_name='ссылка на видеонаблюдение', max_length=200, blank=True, null=True)
    gen_plan = models.ImageField(verbose_name='ген план', upload_to=path_to_property, blank=True, null=True)
    zhk_img = models.ImageField(verbose_name='картинка записаться на просмотр', upload_to=path_to_property, blank=True, null=True)
    facilities = models.ManyToManyField(Facilities, verbose_name='инфраструктура')
    video = models.URLField(verbose_name='видеопрезентация', max_length=200, blank=True, null=True,
        help_text='в конце адреса ?autoplay=1&mute=1, например: https://www.youtube.com/embed/hdi6vkQx?autoplay=1&mute=1')
    has_scraper = models.BooleanField(verbose_name='есть скрапер', default=False)
    is_active = models.BooleanField(verbose_name='активный', default=True)
    mid_rating = models.DecimalField(verbose_name='средний рейтинг новостройки', max_digits=2, decimal_places=1, default=0.0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'ЖК комплексы'
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, ok='_', only_ascii=True)
        super(Property, self).save(*args, **kwargs)
        if self.gen_plan:
            super().save(*args, **kwargs)
            resize_image(self.gen_plan)
        if self.zhk_img:
            super().save(*args, **kwargs)
            resize_image(self.zhk_img)
       

class Rating(models.Model):
    ip = models.CharField(verbose_name='ip адрес', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name='ЖК', related_name='rate')

    def get_rating(self):
        ratings = Rating.objects.filter(property=self.property)
        rate_sum = 0
        try:
            for item in ratings:
                rate_sum += item.star.value
            return round(rate_sum/len(ratings), 1)
        except Exception:
            return 0.0

    class Meta:
        verbose_name_plural = 'Рейтинг'


class PropertyTestimonials(models.Model):
    date = models.DateField(verbose_name='дата публикации', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    testimonial = models.TextField(verbose_name='отзыв', max_length=512)
    fk_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='testimonials')

    def __str__(self):
        return f'{self.date} {self.testimonial}'

    class Meta:
        verbose_name_plural = 'Отзывы о ЖК'


def img_path_small(instance, filename):
    return f'property/{instance.get_build_stage_display()}/{instance.id}/{filename}'


class Buildings(models.Model):
    STAGE_CHOICES = (
        ('b', 'строится'),
        ('p', 'сдан'),
        ('d', 'долгострой'),
    )
    fk_property = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name='ЖК')
    num_dom = models.CharField(max_length=64, verbose_name='номер строения/название дома')
    start_date = models.PositiveIntegerField(verbose_name='год начала строительства', blank=True, null=True)
    build_stage = models.CharField(max_length=15, verbose_name='Стадия строительства', choices=STAGE_CHOICES, default='b')
    addr = models.CharField(max_length=256, verbose_name='Адрес')
    small_img = models.ImageField(upload_to=img_path_small, verbose_name='уменьшенное фото')
    main_contractor = models.CharField(max_length=64, verbose_name='Застройщик')
    building_company = models.CharField(max_length=128, verbose_name='Подрядчик', blank=True)
    pr_declaration = models.CharField(max_length=128, verbose_name='Проектная декларация')
    pr_decl_link = models.URLField(verbose_name='Ссылка на проектную декларацию')
    operation_term = models.CharField(max_length=32, verbose_name='Ввод в эксплуатацию')
    send_keys = models.DateField(verbose_name='Выдача ключей', blank=True, null=True)
    middle_price = models.PositiveIntegerField(verbose_name='Средняя цена за 1 м2', blank=True, null=True)
    property_class = models.CharField(max_length=32, verbose_name='Класс недвижимости')
    wall = models.CharField(max_length=32, verbose_name='Материал стен')
    decoration = models.CharField(max_length=32, verbose_name='Тип отделки')
    free_planning = models.CharField(max_length=20, verbose_name='Свободная планировка')
    floors = models.PositiveSmallIntegerField(verbose_name='Количество этажей')
    q_flats = models.PositiveSmallIntegerField(verbose_name='Количество квартир')
    living_sq = models.PositiveIntegerField(verbose_name='Жилая площадь')
    ceil_height = models.CharField(max_length=15, verbose_name='Высота потолков')
    sales_flats = models.CharField(verbose_name='распроданность квартир', max_length=32, blank=True)
    sales_not_living = models.CharField(verbose_name='распроданность нежилых помещений', max_length=32, blank=True)
    sales_parking = models.CharField(verbose_name='распроданность машиномест', max_length=32, blank=True)
    is_active = models.BooleanField(verbose_name='активный', default=True)

    class Meta:
        verbose_name_plural = 'Объекты недвижимости'
        ordering = ['middle_price', 'operation_term', 'num_dom']

    def __str__(self):
        return self.num_dom


def img_path_photo(instance, filename):
    return f'property/{instance.fk_builging.get_build_stage_display()}/{instance.fk_building.id}/{filename}'


class MainPhotos(models.Model):
    main_img = models.ImageField(upload_to=img_path_photo, verbose_name='фото')
    fk_building = models.ForeignKey(Buildings, on_delete=models.CASCADE, verbose_name='для объекта',
                                    related_name='main_photos')

    class Meta:
        verbose_name_plural = 'Основные фото'


def img_path_build(instance, filename):
    return f'property/{instance.fk_month.fk_building.get_build_stage_display()}/{instance.fk_month.fk_building.id}/building/{instance.fk_month.build_month}/{filename}'


class BuildMonths(models.Model):
    build_month = models.CharField(max_length=20, verbose_name='Месяц строительства')
    fk_building = models.ForeignKey(Buildings, on_delete=models.CASCADE, verbose_name='для объекта',
                                    related_name='build_months')
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        verbose_name_plural = 'Фото объектов по месяцам стр-ва'


class BuildingPhotos(models.Model):
    build_img = models.ImageField(upload_to=img_path_build, blank=True, null=True)
    fk_month = models.ForeignKey(BuildMonths, on_delete=models.CASCADE, verbose_name='месяц',
                                 related_name='build_photos')

    class Meta:
        verbose_name_plural = 'Фото строительства'


class ObjectDocuments(models.Model):
    doc_name = models.CharField(max_length=128, verbose_name='Тип документа')
    doc_date = models.DateTimeField(verbose_name='Дата размещения')
    doc_link = models.URLField(verbose_name='ссылка на документ')
    fk_object = models.ForeignKey(Buildings, on_delete=models.CASCADE, related_name='documents', verbose_name='для объекта')

    def __str__(self):
        return self.doc_name

    class Meta:
        verbose_name_plural = 'Документы недвижимости'


class CheckObjectReadiness(models.Model):
    readiness = models.CharField(max_length=10, verbose_name='Степень готовности')
    initial_date = models.CharField(max_length=32, verbose_name='Срок в первой версии пр декларации')
    changed_date = models.CharField(max_length=32, verbose_name='Срок в текущей версии пр декларации')
    note = models.CharField(max_length=64, verbose_name='Перенос сроков', blank=True)
    fk_object = models.ForeignKey(Buildings, on_delete=models.CASCADE, related_name='check_readiness',
                                  verbose_name='для объекта')

    class Meta:
        verbose_name_plural = 'Перенос плановых сроков строительства'


class CheckTermsPassKeys(models.Model):
    initial_date = models.CharField(
        verbose_name='Первоначальная дата передачи квартир дольщикам', max_length=12)
    changed_date = models.CharField(
        verbose_name='Планируемая дата передачи квартир дольщикам', max_length=12)
    note = models.CharField(max_length=64, verbose_name='Перенос сроков', blank=True)
    fk_object = models.ForeignKey(Buildings, on_delete=models.CASCADE, related_name='check_keys',
                                  verbose_name='для объекта')

    class Meta:
        verbose_name_plural = 'Перенос сроков передачи ключей дольщикам'


def path_to_floor_plans(instance, filename):
    return f'property/floor_img/{instance.fk_build.id}/{filename}'


class PropertyFloorPlans(models.Model):
    fk_build = models.ForeignKey(Buildings, on_delete=models.CASCADE, related_name='floor_plans', verbose_name='для дома ЖК', blank=True, null=True)
    floor = models.CharField(verbose_name='указание этажа/ей', max_length=64, blank=True)
    floor_drawing = models.ImageField(verbose_name='поэтажные планы квартир',  upload_to=path_to_floor_plans, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Поэтажные планы квартир'
    
    def save(self, *args, **kwargs):
        if self.floor_drawing:
            super().save(*args, **kwargs)
            resize_image(self.floor_drawing)


def path_to_decor(instance, filename):
    return f'property/{instance.fk_decor.fk_property.name}/{filename}'


class PropertyDecor(models.Model):
    DECOR_CHOICES = (
        ('Да', 'c отделкой'),
        ('Нет', 'без отделки'),
        ('whitebox', 'white box'),
        ('zak', 'по желанию заказчика'),
        ('-', 'нет данных'),
    )
    fk_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='decors', verbose_name='для ЖК')
    decor = models.CharField(verbose_name='отделка', choices=DECOR_CHOICES, max_length=32, blank=True)
    decor_text = RichTextUploadingField(verbose_name='описание отделки квартир в ЖК', blank=True)

    def __str__(self):
        return self.decor

    class Meta:
        verbose_name_plural = 'Отделка квартир в ЖК'


class PropertyDecorImages(models.Model):
    fk_decor = models.ForeignKey(PropertyDecor, on_delete=models.CASCADE, verbose_name='для отделки', related_name='decor_images')
    decor_img = models.ImageField(verbose_name='картинка отделки ЖК', upload_to=path_to_decor, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Картинки отделки квартир в ЖК'
    
    def save(self, *args, **kwargs):
        if self.decor_img:
            super().save(*args, **kwargs)
            resize_image(self.decor_img)


def img_path(instance, filename):
    return f'flats/{instance.fk_property.name}/{filename}'


class Flats(models.Model):
    FLAT_CHOICES = (
        ('C', 'студия'),
        ('1', '1 комнатная'),
        ('2', '2-х комнатная'),
        ('3', '3-х комнатная'),
        ('4', '4-х комнатная'),
        ('П', 'пентхаус'),
    )
    DECOR_CHOICES = (
        ('Да', 'c отделкой'),
        ('Нет', 'без отделки'),
        ('whitebox', 'white box'),
        ('zak', 'по желанию заказчика'),
        ('-', 'нет данных'),
    )
    STATUS_CHOICES = (
        ('free', 'свободно'),
        ('reserved', 'забронировано'),
        ('sold', 'продано')
    )
    fk_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='flats',
                                  verbose_name='для ЖК')
    fk_building = models.ForeignKey(Buildings, on_delete=models.SET_NULL, blank=True, null=True, related_name='obj_flats', 
                                    verbose_name='для объекта ЖК')
    build_num = models.PositiveSmallIntegerField(verbose_name='Номер дома')
    fl_num = models.PositiveSmallIntegerField(verbose_name='Номер квартиры', blank=True, null=True)
    fl_type = models.CharField(max_length=20, verbose_name='Тип квартиры', choices=FLAT_CHOICES)
    slug = models.SlugField(verbose_name='поле url')
    fl_drawing = models.ImageField(upload_to=img_path, blank=True, null=True)
    floor = models.PositiveSmallIntegerField(verbose_name='Этаж')
    fl_decor = models.CharField(max_length=32, verbose_name='Отделка', choices=DECOR_CHOICES, default='Нет')
    fl_price = models.PositiveIntegerField(verbose_name='Стоимость квартиры', blank=True, null=True)
    fl_sq = models.FloatField(verbose_name='Площадь квартиры')
    fl_status = models.CharField(max_length=20, verbose_name='Статус квартиры', choices=STATUS_CHOICES, default='free')

    def __str__(self):
        return f'{self.fl_type} {self.fl_price}'

    class Meta:
        verbose_name_plural = 'Квартирограмма'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_fl_type_display(), ok='_', only_ascii=True)
        super(Flats, self).save(*args, **kwargs)


class MediaFlats(models.Model):
    FLAT_CHOICES = (
        ('C', 'студия'),
        ('1', '1 комнатная'),
        ('2', '2-х комнатная'),
        ('3', '3-х комнатная'),
        ('4', '4-х комнатная'),
        ('П', 'пентхаус'),
    )
    flat_choice = models.CharField(max_length=32, verbose_name='выберите тип квартиры', choices=FLAT_CHOICES)
    fk_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='flats_media')
    flat_media = models.URLField(max_length=120, verbose_name='медиа данного типа квартиры', help_text='в конце адреса должно быть ?autoplay=1&mute=1')

    def __str__(self):
        return f'{self.fk_property}'

    class Meta:
        verbose_name_plural = 'Медиаконтент квартир'
        ordering = ['fk_property']


class PropertyFeeds(models.Model):
    fk_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='feeds')
    feed = models.URLField(verbose_name='фид с дом клик', max_length=250)

    def __str__(self):
        return f'{self.fk_property}'

    class Meta:
        verbose_name_plural = 'Фиды с дом.клик'
        ordering = ['fk_property']


# def validate_phone(value):
#     result = re.match(r"\+79[0-9]{9}", value)
#     if not result:
#         raise ValidationError('Допускаются только цифры. Вместо "8" вводится "+7"', params={'value': value})
#
#
# class FlatRequest(models.Model):
#     name = models.CharField(max_length=20, verbose_name='Имя')
#     contact_phone = models.CharField(max_length=11, verbose_name='Контактный телефон', validators=[validate_phone])
#     fk_flat = models.ForeignKey(Flats, on_delete=models.CASCADE, related_name='flat_request')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = 'Заявки на покупку квартир'
