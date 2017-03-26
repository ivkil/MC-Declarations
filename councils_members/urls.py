from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<council_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^autocomplete/', views.get_councils_autocomplete, name='get_councils_autocomplete'),
]
