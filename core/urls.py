from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^api/', include(router.urls)),
  url(r'^(\w+)/edit_info$', views.edit_info, name='edit_info'),
  url(r'^(\w+)/edit_edu$', views.edit_edu, name='edit_edu'),
  url(r'^(\w+)/edit_exp$', views.edit_exp, name='edit_exp'),
  url(r'^(\w+)/edit_abroad$', views.edit_abroad, name='edit_abroad'),
  url(r'^(\w+)/edit_honor$', views.edit_honor, name='edit_honor'),
  url(r'^export/(\w+)$', views.export_scholars, name='export_scholars'),
  url(r'^edit_account$', views.edit_account, name='edit_account'),
  url(r'^directory$', views.scholars, name='scholars'),
  url(r'^scholars/class/(\d+)$', views.scholars_by_class, name='scholars_by_class'),
  url(r'^staff$', views.staff, name='staff'),
  url(r'^profile$', views.own_profile, name='own_profile'),
  url(r'^search$', views.search, name='search'),
  url(r'^stats$', views.stats, name='stats'),
  url(r'^married$', views.married, name='married'),
  url(r'^users/activated$', views.activated_users, name='activated_users'),
  url(r'^users/unactivated$', views.unactivated_users, name='unactivated_users'),
  url(r'^activate/users$', views.activate_users, name='activate_users'),
  url(r'^(\w+)/$', views.resolveurl, name='resolveurl'),
  url(r'^(\w+)$', views.profile, name='profile'),
]
