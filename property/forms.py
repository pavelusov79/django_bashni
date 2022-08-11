from pyexpat import model
from django import forms
from django.core.validators import RegexValidator

from property.models import PropertyTestimonials, Rating, RatingStar


class RequestFlatForm(forms.Form):
    name = forms.CharField(max_length=20, label='', required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
    contact_phone = forms.CharField(max_length=12, label='', required=True,
                                    validators=[RegexValidator(regex=r'\+79[0-9]{9}', message='Допускаются только цифры '
                                                'начиная +7, например +79147910011')],
                                    widget=forms.TextInput(attrs={'placeholder': 'Ваш тел. начиная +7, например '
                                                                                 '+79026805500'})
                                    )

    def __init__(self, *args, **kwargs):
        super(RequestFlatForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = PropertyTestimonials
        fields = ["testimonial"]

    def __init__(self, *args, **kwargs):
        super(TestimonialForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Rating
        fields = ['star']
        