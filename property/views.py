from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import ContextMixin, View, TemplateView
from django.views.generic.edit import FormMixin

from property.models import BuildingObjects, City, Flats, Property
from property.forms import RequestFlatForm


class GetContext(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.city
        context['towns'] = City.objects.all()
        return context


class FlatsListView(GetContext, ListView):
    paginate_by = 51

    def get_queryset(self):
        self.city = get_object_or_404(City, city_slug=self.kwargs['city'])
        results = Flats.objects.filter(fk_object__fk_city=self.city)
        zhk = self.request.GET.get('zhk')
        flat_type = self.request.GET.get('flat_type')
        fl_decor = self.request.GET.get('fl_decor')
        price = self.request.GET.get('price')
        param = self.request.GET.get('param')
        reset = self.request.GET.get('reset')
        if zhk:
            results = results.filter(fk_object=int(zhk))
        if flat_type:
            results = results.filter(fl_type__in=flat_type.split(','))
        if fl_decor:
            results = results.filter(fl_decor__in=fl_decor.split(','))
        if price:
            results = results.filter(fl_price__range=(price.split(',')[0], price.split(',')[-1]))
        if param:
            results = results.order_by(param)
        if reset:
            results = Flats.objects.filter(fk_object__fk_city=self.city)
        self.request.session['flat_page'] = self.request.get_full_path()
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property'] = Property.objects.filter(fk_city__city_slug=self.kwargs['city'])
        context['flat_types'] = Flats.FLAT_CHOICES
        context['flat_decors'] = Flats.DECOR_CHOICES
        context['min_price'] = Flats.objects.all().order_by('fl_price').exclude(fl_price=None).first().fl_price
        context['max_price'] = Flats.objects.all().order_by('-fl_price').exclude(fl_price=None).first().fl_price
        return context


class FlatDetailView(FormMixin, DetailView):
    model = Flats
    form_class = RequestFlatForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent'] = False
        try:
            context['page'] = self.request.session['flat_page']
        except KeyError:
            pass
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        context = super().get_context_data()
        name = form.cleaned_data['name']
        contact_phone = form.cleaned_data['contact_phone']
        recipients = ['info.p@111bashni.ru']
        message = f'id квартиры: {self.object.id}\nназвание ЖК: {self.object.fk_object.name}\nтип квартиры:' \
                  f' {self.object.get_fl_type_display() }\nномер дома: {self.object.build_num}\nкв. №: ' \
                  f'{self.object.fl_num}\nэтаж: {self.object.floor}\nплощадь: {self.object.fl_sq} м2\nстоимость: ' \
                  f'{self.object.fl_price} руб.'
        send_mail('заявка на покупку квартиры', f'от: {name}\nконт. тел: {contact_phone}\n{message}',
                  DEFAULT_FROM_EMAIL, recipients)
        context['sent'] = True
        super().form_valid(form)
        return render(self.request, 'property/flats_detail.html', context)

    def get_success_url(self):
        return reverse('flat_detail', kwargs={'city_slug': self.object.fk_object.fk_city.city_slug, 'pk': self.object.pk, 'slug': self.object.slug})


class BuildingObjectsListView(GetContext, ListView):
    paginate_by = 21

    def get_queryset(self):
        self.city = get_object_or_404(City, city_slug=self.kwargs['city'])
        results = BuildingObjects.objects.filter(city=self.city)
        b_class = self.request.GET.get('b_class')
        decor = self.request.GET.get('decor')
        wall = self.request.GET.get('wall')
        param = self.request.GET.get('param')
        price = self.request.GET.get('price')
        reset = self.request.GET.get('reset')
        if b_class:
            results = results.filter(property_class__in=b_class.split(','))
        if wall:
            results = results.filter(wall__in=wall.split(','))
        if decor:
            results = results.filter(decoration__in=decor.split(','))
        if price:
            results = results.filter(middle_price__range=(price.split(',')[0], price.split(',')[-1]))
        if param:
            results = results.order_by(param)
        if reset:
            results = BuildingObjects.objects.filter(city=self.city)
        self.request.session['page'] = self.request.get_full_path()
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['min_price'] = BuildingObjects.objects.filter(city=self.city).order_by('middle_price').exclude(middle_price=None).first().middle_price
        context['max_price'] = BuildingObjects.objects.filter(city=self.city).order_by('-middle_price').exclude(middle_price=None).first().middle_price
        context['property_class'] = list(set(BuildingObjects.objects.filter(city=self.city).values_list('property_class')))
        context['wall_materials'] = list(set(BuildingObjects.objects.filter(city=self.city).values_list('wall')))
        context['decorations'] = list(set(BuildingObjects.objects.filter(city=self.city).values_list('decoration')))
        return context


class BuildingObjectsDetailView(FormMixin, DetailView):
    model = BuildingObjects
    form_class = RequestFlatForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['page'] = self.request.session['page']
        except KeyError:
            pass
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        name = form.cleaned_data['name']
        contact_phone = form.cleaned_data['contact_phone']
        recipients = ['info.p@111bashni.ru']
        message = f'Прошу подобрать квартиру в новостройке: {self.object.name} (ID: {self.object.id}) по адресу: {self.object.addr}.'
        send_mail('заявка на покупку квартиры', f'от: {name}\nконт. тел: {contact_phone}\n{message}',
                  DEFAULT_FROM_EMAIL, recipients)
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





