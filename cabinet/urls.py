from django.urls import path
from cabinet import views

app_name = 'cabinet'


urlpatterns = [
    path('<pk>/main/', views.MainView.as_view(), name='main'),
    path('<pk>/profile/', views.UserVew.as_view(), name='profile'),
    path('<pk>/subscriptions/', views.SubscriptionsView.as_view(), name='subscriptions'),
    path('<pk>/documents/', views.DocsView.as_view(), name='docs'),
    path('<pk>/reservations/', views.ReserveView.as_view(), name='reserve'),
    path('<pk>/loan/', views.LoanView.as_view(), name='loan'),
    path('<pk>/compare/', views.CompareView.as_view(), name='compare'),
]
