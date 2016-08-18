from django.conf.urls import url
from . import views                   #add this line

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^process_account$', views.process_account, name='process_account'),
  url(r'^books$', views.books, name='books'),
  url(r'^books/add$', views.books_add, name='books_add'),
  url(r'^process_review$', views.process_review, name='process_review'),
  url(r'^books/(?P<id>\d+)$', views.show_book, name='show_book'),
  url(r'^delete_review/(?P<review_id>\d+)/(?P<book_id>\d+)$', views.delete_review, name='delete_review'),
  url(r'^user/(?P<id>\d+)$', views.show_user, name='show_user'),
  url(r'^logout$', views.logout, name='logout'),
]
