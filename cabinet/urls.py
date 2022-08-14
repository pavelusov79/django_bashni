from django.urls import path
from cabinet import views

app_name = 'cabinet'


urlpatterns = [
    path('<pk>/main/', views.MainView.as_view(), name='main'),
]
