import emitters
from django.template import Context, loader

class HTMLEmitter(emitters.Emitter):
    """
    JSON emitter, understands timestamps.
    """
    def render(self, request):
        data = self.construct()
        if isinstance(data, list):
            return loader.get_template('objs.html').render(Context({
                'url_prefix' : '/webapi/',
                'objs' : data
                }))
        else:
            return loader.get_template('obj.html').render(Context({
                'url_prefix' : '/webapi/',
                'obj' : data
                }))

emitters.Emitter.register('html', HTMLEmitter, 'text/html')

