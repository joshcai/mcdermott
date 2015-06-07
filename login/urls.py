from django.conf.urls import url

urlpatterns = [
  url(
      r'^login/$', 
      'django.contrib.auth.views.login',
      {'template_name': 'login/login.html'}, 
      name='login'
  ),
  url(
      r'^logout/$', 
      'django.contrib.auth.views.logout',
      {'template_name': 'login/logout.html'}, 
      name='logout'
  ),
  url(
      r'^password_change/$', 
      'django.contrib.auth.views.password_change',
      {'template_name': 'login/password_change.html'}, 
      name='password_change'
  ),
  url(
      r'^password_change_done/$', 
      'django.contrib.auth.views.password_change_done',
      {'template_name': 'login/password_change_done.html'}, 
      name='password_change_done'
  ),
  url(
      r'^password_reset/$', 
      'django.contrib.auth.views.password_reset',
      {'template_name': 'login/password_reset.html'},
      name='password_reset'
  ),
  url(
      r'^password_reset_done/$', 
      'django.contrib.auth.views.password_reset_done',
      {'template_name': 'login/password_reset_done.html'},
      name='password_reset_done'
  ),
  url(
      r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
      'django.contrib.auth.views.password_reset_confirm',
      {'template_name': 'login/password_reset_confirm.html'},
      name='password_reset_confirm'
  ),
  url(
      r'^reset/done/$', 
      'django.contrib.auth.views.password_reset_complete',
      {'template_name': 'login/password_reset_complete.html'},
      name='password_reset_complete'
  ),
]
