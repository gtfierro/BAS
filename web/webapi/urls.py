from django.conf.urls.defaults import patterns, url
import emitters # HACK: patched version of piston.emitters
import html_emitter
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from handlers import TagHandler, QueryHandler, AllHandler, UUIDHandler, UUIDMethodHandler

auth = HttpBasicAuthentication(realm="My Realm")
ad = { 'authentication': auth }

tag_resource = Resource(handler=TagHandler, **ad)
query_resource = Resource(handler=QueryHandler, **ad)
all_resource = Resource(handler=AllHandler, **ad)
uuid_resource = Resource(handler=UUIDHandler, **ad)
uuid_method_resource = Resource(handler=UUIDMethodHandler, **ad)

urlpatterns = patterns('',
    url(r'^t/(?P<tag>\w+)(\.(?P<emitter_format>.+))?$', tag_resource),
    url(r'^query(\.(?P<emitter_format>.+))?$', query_resource),
    url(r'^uuid/(?P<uuid>[a-z0-9-]+)(\.(?P<emitter_format>.+))?$', uuid_resource),
    url(r'^uuid/(?P<uuid>[a-z0-9-]+)/(?P<method>[a-z0-9_-]+)$', uuid_method_resource),
    url(r'^all(\.(?P<emitter_format>.+))?$', all_resource),

    url(r'^geo.html$', 'webapi.views.geo'),
    url(r'^$', 'webapi.views.index'),
)
