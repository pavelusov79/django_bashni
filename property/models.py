from django.db import models
from ckeditor.fields import RichTextField

from slugify import slugify


class City(models.Model):
    city_name = models.CharField(verbose_name='город', max_length=32)
    city_slug = models.SlugField(verbose_name='поле url')
    city_code = models.PositiveSmallIntegerField(verbose_name='код города')

    class Meta:
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.city_name


def img_path_small(instance, filename):
    return f'property/{instance.get_build_stage_display()}/{instance.id}/{filename}'


class BuildingObjects(models.Model):
    STAGE_CHOICES = (
        ('b', 'строится'),
        ('p', 'сдан'),
        ('d', 'долгострой'),
    )
    name = models.CharField(max_length=255, verbose_name='Название ЖК')
    build_stage = models.CharField(max_length=15, verbose_name='Стадия строительства', choices=STAGE_CHOICES, default='b')
    slug = models.SlugField(verbose_name='поле url', max_length=255)
    description = RichTextField(verbose_name='Описание объекта', blank=True)
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
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='build_objects')
    has_flats = models.BooleanField(default=False, verbose_name='Есть ли скрапер квартир')

    class Meta:
        verbose_name_plural = 'Объекты недвижимости'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, ok='_', only_ascii=True)
        super(BuildingObjects, self).save(*args, **kwargs)


def img_path_photo(instance, filename):
    return f'property/{instance.fk_property.get_build_stage_display()}/{instance.fk_property.id}/{filename}'


class MainPhotos(models.Model):
    main_img = models.ImageField(upload_to=img_path_photo, verbose_name='фото')
    fk_property = models.ForeignKey(BuildingObjects, on_delete=models.CASCADE, verbose_name='для объекта',
                                    related_name='main_photos')

    class Meta:
        verbose_name_plural = 'Основные фото'


def img_path_build(instance, filename):
    return f'property/{instance.fk_month.fk_property.get_build_stage_display()}/{instance.fk_month.fk_property.id}/building/{instance.fk_month.build_month}/{filename}'


class BuildMonths(models.Model):
    build_month = models.CharField(max_length=20, verbose_name='Месяц строительства')
    fk_property = models.ForeignKey(BuildingObjects, on_delete=models.CASCADE, verbose_name='для объекта',
                                    related_name='build_months')
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        verbose_name_plural = 'Фото объектов по месяцам стр-ва'


class BuildingPhotos(models.Model):
    build_img = models.ImageField(upload_to=img_path_build, blank=True)
    fk_month = models.ForeignKey(BuildMonths, on_delete=models.CASCADE, verbose_name='месяц',
                                 related_name='build_photos')

    class Meta:
        verbose_name_plural = 'Фото строительства'


class ObjectDocuments(models.Model):
    doc_name = models.CharField(max_length=128, verbose_name='Тип документа')
    doc_date = models.DateTimeField(verbose_name='Дата размещения')
    doc_link = models.URLField(verbose_name='ссылка на документ')
    fk_object = models.ForeignKey(BuildingObjects, on_delete=models.CASCADE, related_name='documents', verbose_name='для объекта')

    def __str__(self):
        return self.doc_name

    class Meta:
        verbose_name_plural = 'Документы недвижимости'


class CheckObjectReadiness(models.Model):
    readiness = models.CharField(max_length=10, verbose_name='Степень готовности')
    initial_date = models.CharField(max_length=32, verbose_name='Срок в первой версии пр декларации')
    changed_date = models.CharField(max_length=32, verbose_name='Срок в текущей версии пр декларации')
    note = models.CharField(max_length=64, verbose_name='Перенос сроков', blank=True)
    fk_object = models.ForeignKey(BuildingObjects, on_delete=models.CASCADE, related_name='check_readiness',
                                  verbose_name='для объекта')

    class Meta:
        verbose_name_plural = 'Перенос плановых сроков строительства'


class CheckTermsPassKeys(models.Model):
    initial_date = models.CharField(verbose_name='Первоначальная дата передачи квартир дольщикам', max_length=12)
    changed_date = models.CharField(verbose_name='Планируемая дата передачи квартир дольщикам', max_length=12)
    note = models.CharField(max_length=64, verbose_name='Перенос сроков', blank=True)
    fk_object = models.ForeignKey(BuildingObjects, on_delete=models.CASCADE, related_name='check_keys',
                                  verbose_name='для объекта')

    class Meta:
        verbose_name_plural = 'Перенос сроков передачи ключей дольщикам'


class Property(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название ЖК')
    address = models.CharField(max_length=256, verbose_name='Адрес ЖК', blank=True)
    fk_city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Для города', related_name='prorerty')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Название ЖК для квартирограммы'


def img_path(instance, filename):
    return f'flats/{instance.fk_object.name}/{filename}'


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
        ('-', 'нет данных'),
        ('whitebox', 'white box'),
    )
    STATUS_CHOICES = (
        ('free', 'свободно'),
        ('reserved', 'забронировано'),
        ('sold', 'продано')
    )
    fk_object = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='flats',
                                  verbose_name='для объекта')
    build_num = models.PositiveSmallIntegerField(verbose_name='Номер дома')
    fl_num = models.PositiveSmallIntegerField(verbose_name='Номер квартиры', blank=True, null=True)
    fl_type = models.CharField(max_length=20, verbose_name='Тип квартиры', choices=FLAT_CHOICES)
    slug = models.SlugField(verbose_name='поле url')
    fl_drawing = models.ImageField(upload_to=img_path, blank=True)
    floor = models.PositiveSmallIntegerField(verbose_name='Этаж')
    fl_decor = models.CharField(max_length=32, verbose_name='Отделка', choices=DECOR_CHOICES, default='Нет')
    fl_price = models.PositiveIntegerField(verbose_name='Стоимость квартиры', blank=True, null=True)
    fl_sq = models.FloatField(verbose_name='Площадь квартиры')
    fl_status = models.CharField(max_length=20, verbose_name='Статус квартиры', choices=STATUS_CHOICES, default='free')

    def __str__(self):
        return f'{self.fl_type} {self.fl_num} {self.fl_price}'

    class Meta:
        verbose_name_plural = 'Квартирограмма'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_fl_type_display(), ok='_', only_ascii=True)
        super(Flats, self).save(*args, **kwargs)


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
