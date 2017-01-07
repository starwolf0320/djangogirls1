from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^prerequisites/$', views.prerequisites, name='prerequisites'),
    url(r'^commitment/$', views.commitment, name='commitment'),
]
