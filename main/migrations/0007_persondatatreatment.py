# Generated by Django 4.0 on 2022-10-30 02:23

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_news_news_visit'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonDataTreatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='заголовок')),
                ('text', ckeditor.fields.RichTextField(verbose_name='текст')),
            ],
            options={
                'verbose_name_plural': 'Обработка персональных данных',
            },
        ),
    ]
