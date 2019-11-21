
import logging
import time
import json

log = logging.getLogger('JSON')

def log_response(wrapped):
    def wrapper(context, request):
        response = wrapped(context, request)
        log.info(_serialize_response(response))
        return response
    return wrapper


def _serialize_response(response):
    x = {}
    x['status']=response.status
    x['headers']=dict(response.headers)
    x['body']=str(response.body)
    y = {'response': x}
    return json.dumps(y)

