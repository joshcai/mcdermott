from django.conf.urls import include, url
from django.contrib import admin
from login import urls as login_urls
from core import urls as core_urls

urlpatterns = [
  url(r'^', include(login_urls)),
  url(r'^', include(core_urls)),
  url(r'^admin/', include(admin.site.urls)),
]
