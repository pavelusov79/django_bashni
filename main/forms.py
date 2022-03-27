from django import forms

from main.models import NewsComment


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ['comment_text']

    def __init__(self, *args, **kwargs):
        super(NewsCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment_text'] = forms.CharField(max_length=512, label='текст комментария',
                                                      widget=forms.Textarea(attrs={'rows': 5}), required=False)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'