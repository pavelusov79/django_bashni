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
]
