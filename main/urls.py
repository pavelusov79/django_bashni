from django.urls import path
from main import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='main'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/<pk>/', views.NewsDetailList.as_view(), name='news_detail'),
    path('news_slug/<tag>/', views.NewsSlugView.as_view(), name='news_slug'),
    path('loan/', views.LoanPageView.as_view(), name='loan'),
    path('repair/', views.RepairPageView.as_view(), name='repair'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('events/', views.EventsView.as_view(), name='events'),
    path('events/<pk>/', views.EventsDetailView.as_view(), name='events_detail'),
    path('policy/', views.PolicyView.as_view(), name='policy'),
    path('news_popular/', views.PopularNewsListView.as_view(), name='news_popular'),
    path('person_data_treatment/', views.PersonDataView.as_view(), name='person_data'),
]

