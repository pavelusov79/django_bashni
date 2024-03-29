# Generated by Django 4.0 on 2022-06-23 10:24

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_alter_propertydecorimages_decor_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='infr_desc',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Инфраструктура'),
        ),
        migrations.AlterField(
            model_name='property',
            name='short_desc',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='property',
            name='territory_desc',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Благоустройство'),
        ),
        migrations.AlterField(
            model_name='property',
            name='work_desc',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Перечень работ'),
        ),
        migrations.AlterField(
            model_name='propertydecor',
            name='decor_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='описание отделки квартир в ЖК'),
        ),
    ]
