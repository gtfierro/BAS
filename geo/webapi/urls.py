from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^t/(?P<tag>\w+)$', 'webapi.views.t', kwargs={'output':'json'}),
    url(r'^t/(?P<tag>\w+).html$', 'webapi.views.t', kwargs={'output':'html'}),

    url(r'^uuid/(?P<uuid>[a-z0-9\-]+)$', 'webapi.views.uuid', kwargs={'output':'json'}),
    url(r'^uuid/(?P<uuid>[a-z0-9\-]+).html$', 'webapi.views.uuid', kwargs={'output':'html'}),

    url(r'^uuid/(?P<uuid>[a-z0-9\-]+)/(?P<method>[a-z0-9_\-]+)$', 'webapi.uuid_method', kwargs={'output':'json'}),
    url(r'^q/html/(?P<string>.+)$', 'webapi.views.query', kwargs={'output': 'html'}),
    url(r'^q/(?P<string>.+)$', 'webapi.views.query', kwargs={'output':'json'}),

    url(r'^$', 'webapi.views.index', kwargs={'output':'json'}),
)
