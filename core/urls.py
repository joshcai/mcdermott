from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^profile/(\w+)/(\w+)$', views.profile, name='profile'),
  url(r'^edit_info$', views.edit_info, name='edit_info'),
]
