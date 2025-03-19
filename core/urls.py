from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home, no_permission
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home, name='home_page'),
    path('no-permission', no_permission, name='no-permission')
]