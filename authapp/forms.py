from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from captcha.fields import CaptchaField


class UserRegisterForm(UserCreationForm):
    captcha = CaptchaField(label='')
    tel = forms.CharField(max_length=11,
                          help_text='Поле необязательное для заполнения',
                          required=False, validators=[RegexValidator(regex='^8[0-9]{10}$',
                          message='Допускаются только цифры начиная с 8-ки, например 84952354422 или 89147900000.')],
                          label='Телефон')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'tel', 'password1', 'password2', 'captcha']

        labels = {
            'username': 'Логин на портале'
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин на портале, телефон или email'
