from django.conf.urls import include, url
from django.contrib import admin
from login import urls as login_urls

urlpatterns = [
  url(r'^', include(login_urls)),
  url(r'^admin/', include(admin.site.urls)),
]
