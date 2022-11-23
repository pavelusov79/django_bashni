from django.contrib.auth.backends import ModelBackend
from django import forms
from django.contrib.auth.models import User
from authapp.models import UserProfile


class PhoneBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        tel = kwargs['username']
        password = kwargs['password']
        try:
            client = UserProfile.objects.get(tel=int(tel))
            print('client = ', client)
            if client.user.check_password(password) is True:
                print('client pass match')
                return client.user
            else:
                raise forms.ValidationError('Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру')
        except Exception:
            pass


class EmailBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        email = kwargs['username']
        password = kwargs['password']
        try:
            client = User.objects.get(email=email)
            print('client = ', client)
            if client.check_password(password) is True:
                print('client pass match')
                return client
            else:
                raise forms.ValidationError('Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру')
        except Exception:
            pass
