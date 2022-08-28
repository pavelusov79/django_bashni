from django.db import models
from django.contrib.auth.models import User

from property.models import Property, Flats


class FavoritesProperty(models.Model):
    property_pk = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name="избранный ЖК")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь",
                             related_name="favorite_properties")

    class Meta:
        verbose_name_plural = "Избранные новостройки"


class FavoritesFlats(models.Model):
    property_pk = models.ForeignKey(Flats, on_delete=models.CASCADE, verbose_name="избранная квартира")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь", related_name="favorite_flats")

    class Meta:
        verbose_name_plural = "Избранные квартиры"
