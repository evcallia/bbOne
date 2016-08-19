from django.conf.urls import url
from . import views                   #add this line


# namespace = belt
urlpatterns = [
  url(r'^main$', views.main, name='main'),
  url(r'^proc_login$', views.proc_login, name='proc_login'),
  url(r'^travels$', views.travels, name='travels'),
  url(r'^travels/add$', views.add, name='add'),
  url(r'^travels/destination/(?P<id>\d+)$', views.show, name='show'),
  url(r'^travels/logout$', views.logout, name='logout'),
  url(r'^travels/join(?P<id>\d+)$', views.join, name='join'),
]
