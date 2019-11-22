import logging
from .decorators import log_response
log = logging.getLogger(__name__)
from pyramid.response import Response
from pyramid.view import (
    view_config,
    notfound_view_config,
    view_defaults
    )


@view_defaults(renderer='home.pt',decorator = log_response)
class TutorialViews:
    def __init__(self, request):
        self.request = request


    @view_config(route_name='home')
    def home(self):
        log.debug('In home view')
        return {'name': 'Home View'}

    @view_config(route_name='hello')
    def hello(self):
        log.debug('In hello view')
        return {'name': 'Hello View'}

def _serialize_res(request):
    x = {}
    x['status']=response.status
    x['headers']=dict(response.headers)
    x['body']=str(response.body)
    y = {'response': x}
    return json.dumps(y)

@notfound_view_config(decorator = log_response)
def notfound_get(request):
    return Response('Not Found', status='404 Not Found')
