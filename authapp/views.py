from django.contrib.auth.views import LoginView, auth_login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from authapp.forms import UserRegisterForm


class UserLoginView(LoginView):
    template_name = 'authapp/login.html'

    def get_success_url(self):
        if 'next' in self.request.POST.keys() and self.request.POST['next'] != '':
            return HttpResponseRedirect(self.request.POST['next'])
        if 'prev_page' in self.request.session.keys():
            return redirect(self.request.session['prev_page'])
        return HttpResponseRedirect(reverse('main'))

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if form.get_user().is_superuser:
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


