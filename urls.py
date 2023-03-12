"""djangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('djangoBlog/', include('djangoBlog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from posts.views import index, by_topic, post_by_slug, post_by_id, search, top_pick, newest
from posts.views import terms_and_conditions, privacy_policy, do_not_sell
from api.views import api

urlpatterns = [
    path('', newest),
    path('newest/', newest, name='newest'),
    path('top-picks/', top_pick, name='top-picks'),

    path('search/', search, name='search'),

    path('topic/<topic>', by_topic, name='post-list-by-topic'),

    path('post/<slug>', post_by_slug, name='post-detail'),
    path('post/id/<id>', post_by_id, name='post-detail-id'),

    path('admin/', admin.site.urls),
    path('secret/api/', api, name='api'),

    path('legal/terms-and-conditions', terms_and_conditions, name='terms-and-conditions'),
    path('legal/privacy-policy', privacy_policy, name='privacy-policy'),
    path('legal/do-not-sell', do_not_sell, name='do-not-sell'),


]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

