from django import forms
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.core.mail import send_mail

from main.models import ImageNews, News, Tags, YoutubeChannel, NewsComment, Events, SitePolicy, PersonDataTreatment


admin.site.register(SitePolicy)
admin.site.register(PersonDataTreatment)


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NewsCommentForm, self).__init__(*args, **kwargs)
        self.fields['failed_moderation'] = forms.CharField(max_length=512, label='поле в случае '
            'отклонения модерации', widget=forms.Textarea(attrs={'rows': 5}), required=False)

    def clean_failed_moderation(self):
        failed_text = self.cleaned_data.get('failed_moderation')
        user = self.cleaned_data.get('user')
        if failed_text:
            send_mail('cooбщение с сайта bashni.pro', failed_text, 'info@111bashni.ru', [user.email, ])

        return failed_text


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ('comment_date', 'user', 'news', 'is_active')
    list_filter = ('is_active', 'failed_moderation')
    form = NewsCommentForm


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('tag_name',)}
    list_display = ('tag_name', 'slug', 'q_ty')

    def q_ty(self, obj):
        return len(News.objects.filter(tags=obj))

    q_ty.short_description = "Кол-во статей"


class ImagesInline(StackedInline):
    model = ImageNews


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'news_visit', 'get_tags')
    list_filter = ('published', 'is_active', 'tags')
    inlines = [ImagesInline]

    def get_tags(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]

    get_tags.short_description = "Тэги"


@admin.register(YoutubeChannel)
class YoutubeChannelAdmin(admin.ModelAdmin):
    list_display = ('date', 'name')
    search_fields = ('name__startswith',)


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'finish_date')
    search_fields = ('title__startswith',)
    list_filter = ('is_active',)
