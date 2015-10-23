from django.conf.urls import url, include

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^view_docs/([a-z]+)/$', views.view_docs, name='view_docs'),
  url(r'^view_docs/$', views.view_docs, name='view_docs'),
  url(r'^create_doc/$', views.create_doc, name='create_doc'),
  url(r'^edit_doc/([0-9]+)$', views.edit_doc, name='edit_doc'),
]
