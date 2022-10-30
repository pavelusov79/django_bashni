import re

from itertools import chain

from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormMixin

from main.models import News, Tags, YoutubeChannel, NewsComment, Events, SitePolicy, PersonDataTreatment
from main.forms import NewsCommentForm
from property.models import Flats, Property, Buildings, City


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.filter(is_active=True).order_by('-published')[:2]
        context['youtube'] = YoutubeChannel.objects.all().order_by('-date')[:4]
        context['events'] = Events.objects.filter(is_active=True).order_by('-start_date')
        prop = Property.objects.all().order_by('-mid_rating').first()
        context['most_popular'] = Buildings.objects.filter(fk_property=prop).first()
        context['towns'] = City.objects.all()
        context['flat_types'] = Flats.FLAT_CHOICES
        context['flat_decors'] = Flats.DECOR_CHOICES
        context['f_dates'] = Flats.objects.distinct('fk_building__operation_term').order_by(
            '-fk_building__operation_term')
        try:
            context['min_price'] = Flats.objects.exclude(fl_price__in=[None, 0]).order_by('fl_price').first().fl_price
            context['max_price'] = Flats.objects.all().order_by('-fl_price').exclude(fl_price=None).first().fl_price
            context['max_sq'] = Flats.objects.all().order_by('-fl_sq').first().fl_sq
            context['min_sq'] = Flats.objects.all().order_by('fl_sq').first().fl_sq
        except Exception:
            context['min_price'] = 0
            context['max_price'] = 0
            context['min_sq'] = 0
            context['max_sq'] = 0
        return context


class NewsListView(ListView):
    paginate_by = 20

    def get_queryset(self):
        return News.objects.filter(is_active=True).order_by('-published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent'] = News.objects.all().order_by('-published')[:4]
        context['popular'] = News.objects.filter(news_visit__gte=10).order_by('-published')[:4]
        return context


class PopularNewsListView(ListView):
    paginate_by = 20

    def get_queryset(self):
        return News.objects.filter(news_visit__gte=10).order_by('-news_visit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent'] = News.objects.all().order_by('-published')[:4]
        context['popular'] = News.objects.filter(news_visit__gte=10).order_by('-published')[:4]
        return context


class NewsDetailList(FormMixin, DetailView):
    model = News
    form_class = NewsCommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = NewsComment.objects.filter(news=self.object, is_active=True)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = self.get_context_data(object=self.object)
        like = self.request.GET.get('likes')
        self.object.news_visit += 1
        self.object.save()

        if like:
            total_likes = int(like) + 1
            self.object.likes = total_likes
            self.object.save()
            return JsonResponse({'data': self.object.likes})
        return self.render_to_response(data)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment_text = form.cleaned_data['comment_text']
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.news = self.object
        comment.save()
        form.save()
        recipients = ['info@111bashni.ru']
        message = f'Необходимо просмотреть комментарий от {self.request.user} к новости: {self.object.title}\nКомментарий: {comment_text}.'
        send_mail('комментарий на валидацию', message, 'it@111bashni.ru', recipients)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('news_detail', kwargs={'pk': self.object.pk})


class NewsSlugView(ListView):
    paginate_by = 20

    def get_queryset(self):
        tags = Tags.objects.get(slug=self.kwargs['tag'])
        return News.objects.filter(tags__slug=tags.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent'] = News.objects.all().order_by('-published')[:4]
        context['popular'] = News.objects.filter(news_visit__gte=10).order_by('-published')[:4]
        return context


class SearchListView(ListView):
    template_name = 'main/search.html'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q')
        query_sets = []
        query_sets.append(News.objects.filter(Q(title__icontains=q) | Q(
            description__icontains=q), is_active=True).order_by('-published'))
        query_sets.append(Property.objects.filter(Q(name__icontains=q) | Q(slug__icontains=q)))
        query_sets.append(Flats.objects.filter(Q(fk_property__name__icontains=q) | Q(fl_type__in=q)))
        self.object_list = list(chain(*query_sets))
        self.request.session['page'] = ''
        self.request.session['flat_page'] = ''
        self.request.session['search'] = self.request.path
        return self.object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_results'] = len(self.object_list)
        return context


class LoanPageView(TemplateView):
    template_name = 'main/in_development_mode.html'


class RepairPageView(TemplateView):
    template_name = 'main/in_development_mode.html'


class FavoritesView(TemplateView):
    template_name = 'main/favorites.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zhk'] = Property.objects.all()
        context['fl'] = Flats.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        fav_obj = self.request.GET.get('fav_obj')
        if fav_obj:
            if re.match(r'\d+_zhk', fav_obj):
                if not self.request.user.is_authenticated:
                    if int(fav_obj.replace('_zhk', '')) in self.request.session['fav_zhk']:
                        self.request.session['fav_zhk'].remove(int(fav_obj.replace('_zhk', '')))
                        self.request.session.modified = True
            elif re.match(r'\d+_fl', fav_obj):
                if not self.request.user.is_authenticated:
                    if int(fav_obj.replace('_fl', '')) in self.request.session['fav_fl']:
                        self.request.session['fav_fl'].remove(int(fav_obj.replace('_fl', '')))
                        self.request.session.modified = True
        return super().get(self, request, *args, **kwargs)


class EventsView(ListView):
    model = Events
    paginate_by = 18


class EventsDetailView(DetailView):
    model = Events


class PolicyView(TemplateView):
    template_name = 'main/policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = SitePolicy.objects.first()
        return context


class PersonDataView(TemplateView):
    template_name = 'main/person_data.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = PersonDataTreatment.objects.first()
        return context


