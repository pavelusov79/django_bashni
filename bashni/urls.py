"""bashni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import bashni.views
from bashni import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.contrib.sitemaps.views import sitemap

from main import views as main_views
from property import views as pr_views

sitemaps = {
    'index': main_views.IndexViewSitemap,
    'static': main_views.StaticViewSitemap,
    'news_slug': main_views.NewsSlugVladivostokSitemapView,
    'news': main_views.NewsSitemapView,
    'property': pr_views.PropertySitemapView,
    'property_detail': pr_views.PropertyDetailSitemapView,
    'flats_detail': pr_views.FlatsDetailSitemapView
}

handler404 = bashni.views.page_not_found_view
handler500 = bashni.views.custom_error_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('authapp.urls', namespace='authapp')),
    path('property/', include('property.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('lk/', include('cabinet.urls', namespace='cabinet')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   
