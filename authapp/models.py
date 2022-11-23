from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    tel = models.PositiveBigIntegerField(verbose_name='телефон', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name_plural = 'Профили пользователей'


