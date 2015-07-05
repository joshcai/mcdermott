from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^api/', include(router.urls)),
  url(r'^edit_info$', views.edit_info, name='edit_info'),
  url(r'^scholars$', views.scholars, name='scholars'),
  url(r'^profile$', views.own_profile, name='own_profile'),
  url(r'^(\w+)$', views.profile, name='profile'),
]