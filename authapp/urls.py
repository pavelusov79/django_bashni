from django.urls import path
from django.contrib.auth.views import LogoutView
from authapp import views

app_name = 'authapp'


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.SingUpView.as_view(), name='register')
]