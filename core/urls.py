from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^edit_info.html$', views.edit_info, name='edit_info')
]
