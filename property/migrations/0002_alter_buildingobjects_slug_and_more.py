# Generated by Django 4.0 on 2022-02-12 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingobjects',
            name='slug',
            field=models.SlugField(max_length=255, verbose_name='поле url'),
        ),
        migrations.AlterField(
            model_name='objectdocuments',
            name='doc_name',
            field=models.CharField(max_length=128, verbose_name='Тип документа'),
        ),
    ]
