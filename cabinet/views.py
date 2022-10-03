import re

from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from cabinet.models import FavoritesProperty, FavoritesFlats
from property.models import Property, Flats


class MainView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'cabinet/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fav_zhk'] = FavoritesProperty.objects.filter(user=self.request.user)
        context['fav_fl'] = FavoritesFlats.objects.filter(user=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        fav_obj = self.request.GET.get('fav_obj')
        print('favorite_cab_obj = ', fav_obj)
        if fav_obj:
            if re.match(r'\d+_zhk', fav_obj):
                fav = FavoritesProperty.objects.get(user=self.request.user,
                                                    property_pk=Property.objects.filter(id=int(fav_obj.replace('_zhk', ''))).first())
                fav.delete()
            elif re.match(r'\d+_fl', fav_obj):
                fav = FavoritesFlats.objects.get(user=self.request.user,
                                                    property_pk=Flats.objects.filter(id=int(fav_obj.replace('_fl', ''))).first())
                fav.delete()
        return super().get(request, *args, **kwargs)


class UserVew(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'cabinet/user.html'


class DocsView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'cabinet/docs.html'


class SubscriptionsView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'cabinet/letter.html'


class ReserveView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'cabinet/reserve.html'


class LoanView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'cabinet/ipoteka.html'


class CompareView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'cabinet/compare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flats'] = Flats.objects.all()
        context['fav_fl'] = [item[0] for item in
                             FavoritesFlats.objects.filter(user=self.request.user).values_list('property_pk')]
        return context

    def get(self, request, *args, **kwargs):
        fav_obj = self.request.GET.get('fav_obj')
        sr_obj = self.request.GET.get('sr_obj')
        sr_empty = self.request.GET.get('sr_empty')
        if fav_obj:
            fav_id = int(fav_obj.replace('_fl', ''))
            if fav_id not in [item[0] for item in
                              FavoritesFlats.objects.filter(user=self.request.user).values_list('property_pk')]:
                fav = FavoritesFlats(user=self.request.user, property_pk=Flats.objects.filter(id=fav_id).first())
                fav.save()
            else:
                fav = FavoritesFlats.objects.get(user=self.request.user,
                                                 property_pk=Flats.objects.filter(id=fav_id).first())
                fav.delete()
        if sr_obj:
            sr_id = int(sr_obj.replace('_sr', ''))
            print('sr_id = ', sr_id)
            self.request.session['sravni_fl'].remove(int(sr_id))
            self.request.session.modified = True
        if sr_empty:
            self.request.session['sravni_fl'] = []
            self.request.session.modified = True
        return super().get(request, *args, **kwargs)


