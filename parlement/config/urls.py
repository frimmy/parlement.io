from django.conf.urls import patterns, include, url

import communities.urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include(communities.urls,'communities')),
    url(r'^admin/', include(admin.site.urls)),
)
