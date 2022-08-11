from property import views
from django.urls import path

urlpatterns = [
    path('<city>/', views.PropertyListView.as_view(), name='property'),
    path('<city_slug>/<int:pk>/<slug>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('<city>/flats/', views.FlatsListView.as_view(), name='sale'),
    path('<city_slug>/flats/<int:pk>/<slug>/', views.FlatDetailView.as_view(), name='flat_detail'),
    path('ajax/check_phone/', views.valid_phone),
]
