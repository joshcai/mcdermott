from django.conf.urls import url, include

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^permissions$', views.permissions, name='permissions'),
  url(r'^app/state$', views.app_state, name='app_state'),
  url(r'^applicants/table$', views.applicant_table, name='applicant_table'),
  url(r'^applicant/add$', views.add_applicant, name='add_applicant'),
  url(r'^applicant/(\w+)$', views.applicant_profile, name='applicant_profile'),
  url(r'^applicant/(\w+)/edit$', views.edit_applicant, name='edit_applicant'),
  url(r'^export$', views.export, name='export'),
]
