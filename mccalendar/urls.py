from django.conf.urls import url, include

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^event_list$', views.event_list, name='event_list'),
  url(r'^event/([0-9]+)$', views.event_detail, name='event_detail'),
  url(r'^create_event$', views.create_event, name='create_event'),
  url(r'^edit_event/([0-9]+)$', views.edit_event, name='edit_event'),
  url(r'^([0-9]+)/([0-9]+)/(prev|next)$', views.month, name='month'),
  url(r'^([0-9]+)/([0-9]+)$', views.month, name='month'),
  url(r'^([0-9]+)/([0-9]+)/([0-9]+)$', views.day, name='day'),
]
