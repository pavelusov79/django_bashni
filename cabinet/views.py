from django.views.generic import DetailView
from django.contrib.auth.models import User


class MainView(DetailView):
    model = User
    template_name = 'cabinet/main.html'



