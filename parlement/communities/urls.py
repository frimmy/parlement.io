from django.conf.urls import patterns, include, url

urlpatterns = patterns('communities.views',
    url(r'^$', 'list', name='list'),
    
    url(r'^community/(?P<name>[a-zA-Z0-9_-]+)/', include(patterns('communities.views',
        url(r'^$', 'view',name='view'),
        url(r'^join/$', 'join',name='join'),
    ))),
    
    url(r'^complete_join_request/(?P<token>[a-f0-9]{40})/$', 'validate_join',name='validate_join'),
)
