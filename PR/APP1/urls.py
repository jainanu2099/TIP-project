from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.get_info, name='get_info'),
    path('', views.display, name='display')
]

urlpatterns += staticfiles_urlpatterns()
