# Generated by Django 4.0 on 2022-07-10 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0010_alter_property_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFlats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flat_choice', models.CharField(choices=[('C', 'студия'), ('1', '1 комнатная'), ('2', '2-х комнатная'), ('3', '3-х комнатная'), ('4', '4-х комнатная'), ('П', 'пентхаус')], max_length=32, verbose_name='выберите тип квартиры')),
                ('flat_media', models.URLField(help_text='в конце адреса должно быть ?autoplay=1&mute=1', max_length=120, verbose_name='медиа данного типа квартиры')),
                ('fk_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flats_media', to='property.property')),
            ],
            options={
                'verbose_name_plural': 'Медиаконтент квартир',
            },
        ),
    ]
