import datetime
import re

from django.contrib.sitemaps import Sitemap
from django.db.models import Max, F
from django.core.mail import send_mail
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin

from property.models import BuildMonths, BuildingPhotos, Buildings, City, Flats, Property, PropertyTestimonials, Rating, PropertyDecor
from property.forms import RequestFlatForm, TestimonialForm, RatingForm
from main.models import News
from cabinet.models import FavoritesFlats, FavoritesProperty


class GetContext(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.city
        context['towns'] = City.objects.all()
        return context


class FlatsListView(GetContext, ListView):
    paginate_by = 24

    def get_queryset(self):
        self.city = get_object_or_404(City, city_slug=self.kwargs['city'])
        results = Flats.objects.filter(fk_property__city=self.city).order_by('?')
        zhk = self.request.GET.get('zhk')
        flat_type = self.request.GET.get('flat_type')
        fl_decor = self.request.GET.get('fl_decor')
        price = self.request.GET.get('price')
        floor = self.request.GET.get('floor')
        square = self.request.GET.get('square')
        date = self.request.GET.get('date')
        param = self.request.GET.get('param')
        district = self.request.GET.get('district')
        reset = self.request.GET.get('reset')
        fav_obj = self.request.GET.get('fav_obj')
        sr_obj = self.request.GET.get('sr_obj')
        self.request.session['flat_page'] = self.request.get_full_path()
        if 'fav_fl' not in self.request.session.keys():
            self.request.session['fav_fl'] = []
        if 'sravni_fl' not in self.request.session.keys():
            self.request.session['sravni_fl'] = []
        if fav_obj:
            if not self.request.user.is_authenticated:
                if int(fav_obj) not in self.request.session['fav_fl']:
                    self.request.session['fav_fl'].append(int(fav_obj))
                    self.request.session.modified = True
                else:
                    self.request.session['fav_fl'].remove(int(fav_obj))
                    self.request.session.modified = True
            else:
                fav_id = int(fav_obj.replace('_fl', ''))
                if fav_id not in [item[0] for item in FavoritesFlats.objects.filter(user=self.request.user).values_list('property_pk')]:
                    fav = FavoritesFlats(user=self.request.user, property_pk=Flats.objects.filter(id=fav_id).first())
                    fav.save()
                else:
                    fav = FavoritesFlats.objects.get(user=self.request.user,
                                           property_pk=Flats.objects.filter(id=fav_id).first())
                    fav.delete()
        if sr_obj:
            if re.search(r'\w1', sr_obj):
                sr_id = int(sr_obj.replace('_sr1', ''))
            else:
                sr_id = int(sr_obj.replace('_sr', ''))
            if int(sr_id) not in self.request.session['sravni_fl']:
                self.request.session['sravni_fl'].append(int(sr_id))
                self.request.session.modified = True
            else:
                self.request.session['sravni_fl'].remove(int(sr_id))
                self.request.session.modified = True

        if zhk:
            results = results.filter(Q(fk_property__name__icontains=zhk) | Q(fk_building__addr__icontains=zhk))
        if date:
            results = results.filter(fk_building__operation_term=date)
        if district:
            results = results.filter(fk_property__district__icontains=district)
        if flat_type:
            if '3' in flat_type:
               results = results.filter(fl_type__gte='3') 
            else:
                results = results.filter(fl_type__in=flat_type)
        if fl_decor:
            results = results.filter(fl_decor=fl_decor)
        if price:
            results = results.filter(fl_price__range=(price.split(',')[0], price.split(',')[-1]))
        if floor:
            results = results.filter(floor__range=(floor.split(',')[0], floor.split(',')[-1]))
        if square:
            results = results.filter(fl_sq__range=(square.split(',')[0], square.split(',')[-1]))
        if param:
            results = results.order_by(param)
        if reset:
            results = Flats.objects.filter(fk_property__city=self.city).order_by('?')
            self.request.session['flat_page'] = self.request.path
        
        self.request.session['search'] = ''
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property'] = Property.objects.filter(city__city_slug=self.kwargs['city'], has_scraper=True)
        context['property_all'] = Property.objects.filter(city__city_slug=self.kwargs['city'])
        context['flat_types'] = Flats.FLAT_CHOICES
        context['flat_decors'] = Flats.DECOR_CHOICES
        context['f_dates'] = Flats.objects.distinct('fk_building__operation_term').order_by('-fk_building__operation_term')
        context['districts'] = Flats.objects.distinct('fk_property__district')
        try:
            context['min_price'] = Flats.objects.exclude(fl_price__in=[None, 0]).order_by('fl_price').first().fl_price
            context['max_price'] = Flats.objects.all().order_by('-fl_price').exclude(fl_price=None).first().fl_price
            context['max_sq'] = Flats.objects.all().order_by('-fl_sq').first().fl_sq
            context['min_sq'] = Flats.objects.all().order_by('fl_sq').first().fl_sq
            context['max_fl'] = Flats.objects.all().order_by('-floor').first().floor
        except Exception:
            context['min_price'] = 0
            context['max_price'] = 0
            context['min_sq'] = 0
            context['max_sq'] = 0
            context['max_fl'] = 25
        if self.request.user.is_authenticated:
            context['fav_fl'] = [item[0] for item in FavoritesFlats.objects.filter(user=self.request.user).values_list('property_pk')]
        return context


class FlatDetailView(FormMixin, DetailView):
    model = Flats
    form_class = RequestFlatForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['page'] = self.request.session['flat_page']
        except KeyError:
            context['page'] = ''
        try:
            context['search'] = self.request.session['search']
        except KeyError:
            context['search'] = ''
        if self.object.fl_price:
            context['similar'] = Flats.objects.filter(fk_property=self.object.fk_property, fl_price__range=((self.object.fl_price - 200000), (self.object.fl_price + 200000)), fl_sq__range=((self.object.fl_sq - 10), (self.object.fl_sq + 10))).exclude(fl_price__in=[None, 0]).order_by('fl_price')
        else:
            context['similar'] = Flats.objects.filter(fk_property=self.object.fk_property, fl_sq__range=((self.object.fl_sq - 10), (self.object.fl_sq + 10))).order_by('fl_sq')
        context['otdelka'] = PropertyDecor.objects.filter(fk_property=self.object.fk_property)
        if self.request.user.is_authenticated:
            context['fav_fl'] = [item[0] for item in FavoritesFlats.objects.filter(user=self.request.user).values_list('property_pk')]
        return context

    def get(self, request, *args, **kwargs):
        fav_obj = self.request.GET.get('fav_obj')
        print('fav_obj= ', fav_obj)
        if 'fav_fl' not in self.request.session.keys():
            self.request.session['fav_fl'] = []
        if fav_obj:
            if not self.request.user.is_authenticated:
                if int(fav_obj) not in self.request.session['fav_fl']:
                    self.request.session['fav_fl'].append(int(fav_obj))
                    self.request.session.modified = True
                else:
                    self.request.session['fav_fl'].remove(int(fav_obj))
                    self.request.session.modified = True
            else:
                fav_id = int(fav_obj.replace('_fl', ''))
                if fav_id not in [item[0] for item in
                                  FavoritesFlats.objects.filter(user=self.request.user).values_list('property_pk')]:
                    fav = FavoritesFlats(user=self.request.user, property_pk=Flats.objects.filter(id=fav_id).first())
                    fav.save()
                else:
                    fav = FavoritesFlats.objects.get(user=self.request.user,
                                                     property_pk=Flats.objects.filter(id=fav_id).first())
                    fav.delete()
        return super().get(self, request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        fio = request.POST.get('fio')
        tel_ipoteka = request.POST.get('tel-ip')
        if fio and tel_ipoteka:
            recipients = ['crm@111bashni.ru']
            message = f'Заяка на расчет ипотеки квартиры { self.object.get_fl_type_display() } в ЖК { self.object.fk_property.name }, дом: {self.object.fk_building.num_dom }, этаж: {self.object.floor}, № кв: {self.object.fl_num}\nстоимость квартиры: {self.object.fl_price} руб.\nпервоначальный взнос: {request.POST.get("calc2")} руб.\nФИО: {fio}\nтел: +7{tel_ipoteka}'
            send_mail('Заяка на расчет ипотеки квартиры', message, 'it@111bashni.ru', recipients) 
        
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        context = super().get_context_data()
        name = form.cleaned_data['name']
        contact_phone = form.cleaned_data['contact_phone']
        recipients = ['crm@111bashni.ru']
        message = f'id квартиры: {self.object.id}\nназвание ЖК: {self.object.fk_property.name}\nтип квартиры:' \
                  f' { self.object.get_fl_type_display() }\nномер дома: {self.object.build_num}\nкв. №: ' \
                  f'{self.object.fl_num}\nэтаж: {self.object.floor}\nплощадь: {self.object.fl_sq} м2\nстоимость: ' \
                  f'{self.object.fl_price} руб.'
        send_mail('заявка на наличие квартиры', f'от: {name}\nконт. тел: {contact_phone}\n{message}',
                  'it@111bashni.ru', recipients)
        super().form_valid(form)
        return render(self.request, 'property/flats_detail.html', context)

    def get_success_url(self):
        return reverse('flat_detail', kwargs={'city_slug': self.object.fk_property.city.city_slug, 'pk': self.object.pk, 'slug': self.object.slug})


class PropertyListView(GetContext, ListView):
    paginate_by = 24
    template_name = 'property/property_list.html'
    context_object_name = 'results'

    def get_queryset(self):
        self.city = get_object_or_404(City, city_slug=self.kwargs['city'])
        results = Property.objects.filter(city=self.city).order_by('-has_scraper', 'name')
        zhk = self.request.GET.get('zhk')
        date = self.request.GET.get('date')
        decor = self.request.GET.get('decor')
        district = self.request.GET.get('district')
        param = self.request.GET.get('param')
        price = self.request.GET.get('price')
        reset = self.request.GET.get('reset')
        fav_obj = self.request.GET.get('fav_obj')
        sr_obj = self.request.GET.get('sr_obj')
        self.request.session['page'] = self.request.get_full_path()
        if 'fav_zhk' not in self.request.session.keys():
            self.request.session['fav_zhk'] = []
        if 'sravni_zhk' not in self.request.session.keys():
            self.request.session['sravni_zhk'] = []
        if fav_obj:
            if not self.request.user.is_authenticated:
                if int(fav_obj) not in self.request.session['fav_zhk']:
                    self.request.session['fav_zhk'].append(int(fav_obj))
                    self.request.session.modified = True
                else:
                    self.request.session['fav_zhk'].remove(int(fav_obj))
                    self.request.session.modified = True
            else:
                fav_id = int(fav_obj.replace('_zhk', ''))
                if fav_id not in [item[0] for item in FavoritesProperty.objects.filter(user=self.request.user).values_list('property_pk')]:
                    fav = FavoritesProperty(user=self.request.user, property_pk=Property.objects.filter(id=fav_id).first())
                    fav.save()
                else:
                    fav = FavoritesProperty.objects.get(user=self.request.user,
                                                        property_pk=Property.objects.filter(id=fav_id).first())
                    fav.delete()

        if sr_obj:
            if re.search(r'\w1', sr_obj):
                sr_id = int(sr_obj.replace('_sr1', ''))
            else:
                sr_id = int(sr_obj.replace('_sr', ''))
            if int(sr_id) not in self.request.session['sravni_zhk']:
                self.request.session['sravni_zhk'].append(int(sr_id))
                self.request.session.modified = True
            else:
                self.request.session['sravni_zhk'].remove(int(sr_id))
                self.request.session.modified = True
        if zhk:
            results = list(set(results.filter(Q(name__icontains=zhk) | Q(buildings__addr__icontains=zhk))))
        if district:
            results = results.filter(district=district)
        if date:
            results = list(set(results.filter(buildings__operation_term=date)))
        if decor:
            results = list(set(results.filter(buildings__decoration=decor)))
        if price:
            results = list(set(results.filter(buildings__middle_price__range=(price.split(',')[0], price.split(',')[-1]))))
        if param:
            if param == 'buildings__middle_price':
                results = results.annotate(custom_order=Max('buildings__middle_price')).exclude(buildings__middle_price=None).order_by('custom_order')
            elif param == '-buildings__middle_price':
                results = results.annotate(custom_order=Max('buildings__middle_price')).exclude(buildings__middle_price=None).order_by('custom_order').reverse
            elif param == 'mid_rating':
                results = results.order_by('-mid_rating', 'name')
            elif param == 'buildings__send_keys':
                results = results.annotate(custom_order=Max('buildings__send_keys')).order_by('custom_order')
        if reset:
            results = Property.objects.filter(city=self.city).order_by('-has_scraper', 'name')
            self.request.session['page'] = self.request.path
        self.request.session['search'] = ''
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['fav_zhk'] = [item[0] for item in FavoritesProperty.objects.filter(user=self.request.user).values_list('property_pk')]
        try:
            context['min_price'] = Buildings.objects.filter(fk_property__city=self.city).order_by('middle_price').exclude(middle_price=None).first().middle_price
            context['max_price'] = Buildings.objects.filter(fk_property__city=self.city).order_by('-middle_price').exclude(middle_price=None).first().middle_price
        except Exception:
            context['min_price'] = 0
            context['max_price'] = 0
            # context['fav_zhk'] = ''
        # context['property_class'] = list(set(Buildings.objects.filter(fk_property__city=self.city).values_list('property_class')))
        # context['wall_materials'] = list(set(Buildings.objects.filter(fk_property__city=self.city).values_list('wall')))
        context['decorations'] = list(set(Buildings.objects.filter(fk_property__city=self.city).values_list('decoration')))
        context['districts'] = Property.objects.distinct('district').order_by('district')
        context['f_dates'] = Buildings.objects.distinct('operation_term').order_by('operation_term'.split()[-1])
        return context


class PropertyDetailView(FormMixin, DetailView):
    model = Property
    form_class = TestimonialForm

    def get(self, request, *args, **kwargs):
        fav_obj = self.request.GET.get('fav_obj')
        if 'fav_zhk' not in self.request.session.keys():
            self.request.session['fav_zhk'] = []
        if fav_obj:
            if not self.request.user.is_authenticated:
                if int(fav_obj) not in self.request.session['fav_zhk']:
                    self.request.session['fav_zhk'].append(int(fav_obj))
                    self.request.session.modified = True
                else:
                    self.request.session['fav_zhk'].remove(int(fav_obj))
                    self.request.session.modified = True
            else:
                fav_id = int(fav_obj.replace('_zhk', ''))
                if fav_id not in [item[0] for item in FavoritesProperty.objects.filter(user=self.request.user).values_list('property_pk')]:
                    fav = FavoritesProperty(user=self.request.user, property_pk=Property.objects.filter(id=fav_id).first())
                    fav.save()
                else:
                    fav = FavoritesProperty.objects.get(user=self.request.user,
                                           property_pk=Property.objects.filter(id=fav_id).first())
                    fav.delete()
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['fav_zhk'] = [item[0] for item in FavoritesProperty.objects.filter(user=self.request.user).values_list('property_pk')]
        try:
            context['page'] = self.request.session['page']
        except KeyError:
            context['page'] = ''
        months = BuildMonths.objects.filter(fk_building=Buildings.objects.filter(fk_property=self.object).first()).values_list('build_month')
        if self.request.GET.get('num_dom'):
            context['dom'] = self.request.GET.get('num_dom')
            context['building'] = Buildings.objects.filter(fk_property=self.object, num_dom=self.request.GET.get('num_dom')).first()
            months = BuildMonths.objects.filter(fk_building=Buildings.objects.filter(fk_property=self.object, num_dom=self.request.GET.get('num_dom')).first()).values_list('build_month')
        l = []
        for i in months:
            l.append(i[0].split(',')[-1].strip())
        context['build_year'] = set(l)
        context['build_news'] = News.objects.filter(tags__tag_name__icontains=self.object.name).order_by('-published').first()
        context['news'] = News.objects.filter(tags__tag_name=self.object.city.city_name).order_by('-published').first()
        context['similar_obj'] = Property.objects.filter(district__icontains=self.object.district.replace('район', "").strip(), city__city_name=self.object.city.city_name).order_by('name').exclude(name=self.object.name)
        context['dates'] = Buildings.objects.filter(fk_property=self.object).distinct('operation_term').order_by('-operation_term')
        # context['dates'] = set([datetime.datetime.strftime(i[0], "%Y") for i in l])
        context['fil_flats'] = Flats.objects.filter(fk_property=self.object).distinct('fl_type')
        el = self.request.GET.get('ind_el')
        type_of_flat = self.request.GET.get('type_of_flat')
        if type_of_flat:
            context['type_flat'] = type_of_flat
            context['flats_d'] = Flats.objects.filter(fk_property=self.object, fl_type=type_of_flat).exclude(fl_drawing='').exclude(fl_price=None).order_by('fl_sq').distinct('fl_sq')
            if context['flats_d']:
                context['current_price'] = context['flats_d'][0].fl_price
            if el and context['flats_d']:
                context['current_price'] = context['flats_d'][int(el)].fl_price
                print('price ', context['flats_d'][int(el)].fl_price)
        else:
            try:
                context['type_flat'] = context['fil_flats'][0].fl_type
            except IndexError:
                context['type_flat'] = '1'
            try:
                context['flats_d'] = Flats.objects.filter(fk_property=self.object, fl_type=context['fil_flats'][0].fl_type).exclude(fl_drawing='').exclude(fl_price=None).order_by('fl_sq').distinct('fl_sq')
            except IndexError:
                context['flats_d'] = ''
            if context['flats_d']:
                context['current_price'] = context['flats_d'][0].fl_price
        if el and context['flats_d']:
            context['current_price'] = context['flats_d'][int(el)].fl_price
        context['testimonials'] = PropertyTestimonials.objects.filter(fk_property=self.object).order_by('-date')
        context['star_form'] = RatingForm()
        context['request_form'] = RequestFlatForm()

        print('fil_flats = ', context['fil_flats'])
        return context

    def get_client_ip(self):
        ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        star_id = self.request.POST.get('star')
        if star_id:
            star_form = RatingForm(request.POST)
            if star_form.is_valid():
                Rating.objects.update_or_create(
                    ip=self.get_client_ip(),
                    property=self.object,
                    defaults={'star_id': int(star_id)}
                )
                self.object.mid_rating = self.object.rate.first().get_rating()
                self.object.save()
        name = request.POST.get('name')
        tel = request.POST.get('contact_phone')
        if name and tel:
            recipients = ['crm@111bashni.ru']
            message = f'Поступила заяка на просмотр ЖК:\nжилой комплекс: {self.object.name}\nот: {name}\nконтактный тел: {tel}'
            send_mail('Заяка на просмотр ЖК', message, 'it@111bashni.ru', recipients)       
        fio = request.POST.get('fio')
        tel_ipoteka = request.POST.get('tel-ip')
        if fio and tel_ipoteka:
            recipients = ['crm@111bashni.ru']
            message = f'Заяка на расчет ипотеки:\nстоимость жилья: {request.POST.get("calc1")} руб.\nпервоначальный взнос: {request.POST.get("calc2")} руб.\nФИО: {fio}\nтел: +7{tel_ipoteka}'
            send_mail('Заяка на расчет ипотеки', message, 'it@111bashni.ru', recipients) 
        
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        testimonial = form.save(commit=False)
        testimonial.user = self.request.user
        testimonial.fk_property = self.object
        testimonial.save()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('property_detail',
                       kwargs={'city_slug': self.object.city.city_slug, 'pk': self.object.pk,
                               'slug': self.object.slug})


def valid_phone(request):
    phone = request.GET.get('contact_phone')
    response = {
        'valid_phone': phone
    }
    return JsonResponse(response)


#______________Sitemap views_______________
class PropertyDetailSitemapView(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Property.objects.filter(is_active=True)

    def location(self, item):
        return f'/property/{item.city.city_slug}/{item.pk}/{item.slug}/'


class FlatsDetailSitemapView(Sitemap):
    def items(self):
        return Flats.objects.filter(fl_status='free')

    def location(self, item):
        return f'/property/{item.fk_property.city.city_slug}/flats/{item.pk}/{item.slug}/'


class PropertySitemapView(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ['property']

    def location(self, item):
        return '/property/vladivostok/'








