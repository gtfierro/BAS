from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^t/(?P<tag>\w+)$', 'webapi.views.t', kwargs={'output':'json'}),
    url(r'^t/(?P<tag>\w+).html$', 'webapi.views.t', kwargs={'output':'html'}),

    url(r'^all$', 'webapi.views.all_objs', kwargs={'output':'json'}),
    url(r'^all.html$', 'webapi.views.all_objs', kwargs={'output':'html'}),

    url(r'^uuid/(?P<uuid>[a-z0-9-]+)$', 'webapi.views.uuid', kwargs={'output':'json'}),
    url(r'^uuid/(?P<uuid>[a-z0-9-]+).html$', 'webapi.views.uuid', kwargs={'output':'html'}),

    url(r'^uuid/(?P<uuid>[a-z0-9-]{35})/(?P<method>[a-z0-9_-]+)$', 'webapi.views.uuid_method', kwargs={'output':'json'}),

    url(r'^query.html$', 'webapi.views.query', kwargs={'output': 'html'}),
    url(r'^query$', 'webapi.views.query', kwargs={'output':'json'}),
    url(r'^$', 'webapi.views.index', kwargs={'output':'json'}),
)
