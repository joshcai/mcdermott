from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^edit_info$', views.edit_info, name='edit_info'),
  url(r'^scholars$', views.scholars, name='scholars'),
  url(r'^profile$', views.own_profile, name='own_profile'),
  url(r'^(\w+)$', views.profile, name='profile'),
]