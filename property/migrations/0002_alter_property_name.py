# Generated by Django 4.0 on 2022-05-04 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='Название ЖК'),
        ),
    ]
