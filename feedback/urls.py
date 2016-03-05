from django.conf.urls import url, include

from . import views

urlpatterns = [
  url(r'^$', views.index_redirect, name='index_redirect'),
  url(r'^grant/permission/(\w+)$', views.grant_permission, name='grant_permission'),
  url(r'^revoke/permission/(\w+)$', views.revoke_permission, name='revoke_permission'),
  url(r'^app/state$', views.app_state, name='app_state'),
  url(r'^(\w+)/applicants/table$', views.applicant_table, name='applicant_table'),
  url(r'^(\w+)/applicants/table/ratings$', views.applicant_table_ratings, name='applicant_table_ratings'),
  url(r'^(\w+)/applicant/add$', views.add_applicant, name='add_applicant'),
  url(r'^(\w+)/favorite/applicant/(\w+)$', views.favorite_applicant, name='favorite_applicant'),
  url(r'^(\w+)/shortlist/applicant/(\w+)$', views.shortlist_applicant, name='shortlist_applicant'),
  url(r'^(\w+)/applicant/(\w+)$', views.applicant_profile, name='applicant_profile'),
  url(r'^(\w+)/applicant/(\w+)/edit$', views.edit_applicant, name='edit_applicant'),
  url(r'^(\w+)/export$', views.export_fw, name='export'),
  url(r'^(\w+)$', views.index, name='index'),
]
