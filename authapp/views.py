from django.contrib.auth.views import LoginView, auth_login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from authapp.forms import UserRegisterForm, MyAuthenticationForm
from cabinet.models import FavoritesProperty, FavoritesFlats
from property.models import Property, Flats


class UserLoginView(LoginView):
    template_name = 'authapp/login.html'
    authentication_form = MyAuthenticationForm

    def get_success_url(self):
        if 'fav_zhk' in self.request.session.keys():
            for item in self.request.session['fav_zhk']:
                favorites_db = [item.property_pk.id for item in FavoritesProperty.objects.filter(user=self.request.user)]
                if item not in favorites_db:
                    add_fav = FavoritesProperty(property_pk=Property.objects.filter(id=item).first(), user=self.request.user)
                    add_fav.save()
        if 'fav_fl' in self.request.session.keys():
            for item in self.request.session['fav_fl']:
                favorites_db = [item.property_pk.id for item in FavoritesFlats.objects.filter(user=self.request.user)]
                if item not in favorites_db:
                    add_fav = FavoritesFlats(property_pk=Flats.objects.filter(id=item).first(), user=self.request.user)
                    add_fav.save()
        if 'next' in self.request.POST.keys() and self.request.POST['next'] == '/favorites/':
            return HttpResponseRedirect(reverse('cabinet:main', kwargs={'pk': self.request.user.pk}))
        if 'next' in self.request.POST.keys() and self.request.POST['next'] != '':
            return HttpResponseRedirect(self.request.POST['next'])
        if 'prev_page' in self.request.session.keys():
            if self.request.session['prev_page'] == '/favorites/':
                return HttpResponseRedirect(reverse('cabinet:main', kwargs={'pk': self.request.user.pk}))
            else:
                return redirect(self.request.session['prev_page'])
        return HttpResponseRedirect(reverse('main'))

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if form.get_user().is_staff:
            return HttpResponseRedirect(reverse('admin:index'))
        else:
            return self.get_success_url()


class SingUpView(CreateView):
    form_class = UserRegisterForm
    template_name = 'authapp/register.html'

    def get_success_url(self):
        return reverse('authapp:login')

    def get(self, request, *args, **kwargs):
        request.session.set_expiry(300)
        request.session['prev_page'] = request.META.get('HTTP_REFERER')
        return super().get(request, *args, **kwargs)


