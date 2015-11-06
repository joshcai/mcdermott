from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from login import urls as login_urls
from mccalendar import urls as mccalendar_urls
from documents import urls as documents_urls
from feedback import urls as feedback_urls
from issues import urls as issues_urls
from core import urls as core_urls

urlpatterns = [
  url(r'^', include(login_urls)),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^calendar/', include(mccalendar_urls, namespace='mccalendar')),
  url(r'^documents/', include(documents_urls, namespace='documents')),
  url(r'^feedback/', include(feedback_urls, namespace='feedback')),
  url(r'^issues/', include(issues_urls, namespace='issues')),

  # core_urls has to be at the end, because the last match in core_urls
  # will match anything
  url(r'^', include(core_urls)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
