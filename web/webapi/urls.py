from django.conf.urls.defaults import patterns, url
import emitters # HACK: patched version of piston.emitters
import html_emitter
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from handlers import TagHandler, QueryHandler, AllHandler, UUIDHandler, UUIDMethodHandler


tag_resource = Resource(handler=TagHandler)
query_resource = Resource(handler=QueryHandler)
all_resource = Resource(handler=AllHandler)
uuid_resource = Resource(handler=UUIDHandler)
uuid_method_resource = Resource(handler=UUIDMethodHandler)

urlpatterns = patterns('',
    url(r'^t/(?P<tag>\w+)(\.(?P<emitter_format>.+))?$', tag_resource),
    url(r'^query(\.(?P<emitter_format>.+))?$', query_resource),
    url(r'^uuid/(?P<uuid>[a-z0-9-]+)(\.(?P<emitter_format>.+))?$', uuid_resource),
    url(r'^uuid/(?P<uuid>[a-z0-9-]+)/(?P<method>[a-z0-9_-]+)$', uuid_method_resource),
    url(r'^all(\.(?P<emitter_format>.+))?$', all_resource),

    url(r'^geo.html$', 'webapi.views.geo'),
    url(r'^index.html$', 'webapi.views.index'),
    url(r'^$', 'django.contrib.auth.views.login', {
          'template_name': 'login.html'})
)
