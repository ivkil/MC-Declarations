from django.conf.urls import url, include
from django.contrib import admin

from councils_members import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^councils/', include('councils_members.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^about/', views.about, name='about'),
]
