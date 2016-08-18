from django.conf.urls import url
from . import views                   #add this line

urlpatterns = [
  url(r'^$', views.index, name='index'),
  # url(r'^users$', views.show, name=''),
  # url(r'^$', views.index, name=''),
  # url(r'^users$', views.show, name=''),
  # url(r'^$', views.index, name=''),
  # url(r'^users$', views.show, name=''),
]
