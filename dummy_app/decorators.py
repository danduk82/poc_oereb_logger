
import logging
import time
import json

log = logging.getLogger('JSON')

def log_response(wrapped):
    def wrapper(context, request):
        response = wrapped(context, request)
#        import ipdb; ipdb.set_trace()
        ret_dict = _serialize_response(response)
        ret_dict.update(_serialize_request(request))
        log.info(json.dumps(ret_dict))
        return response
    return wrapper


def _serialize_response(response):
    x = {}
    x['status']=response.status
    x['headers']=dict(response.headers)
    return {'response': x}

def _serialize_request(request):
    x = {}
    x['headers']=dict(request.headers)
    x['traversed']=str(request.traversed)
    x['parameters']=dict(request.GET)
    x['path']=str(request.path)
    x['view_name']=str(request.view_name)
    return {'request': x}
