from django.conf.urls import patterns, include, url

import communities.urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include(communities.urls,'communities')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'django.contrib.auth.views.logout', { 'next_page':"/" }, name="logout"),
    url(r'^login/$', 'django.contrib.auth.views.login',name="login"),
)
