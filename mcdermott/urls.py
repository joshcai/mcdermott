from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from login import urls as login_urls
from core import urls as core_urls

urlpatterns = [
  url(r'^', include(login_urls)),
  url(r'^admin/', include(admin.site.urls)),
  # core_urls has to be at the end, because the last match in core_urls
  # will match anything
  url(r'^', include(core_urls)),
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
