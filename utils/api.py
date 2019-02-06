import json

from django.http import HttpResponse


class Api:
    class Error(Exception):
        pass

    def __init__(self):
        self.apis = {}

    def __call__(self, request, *args, **kwargs):
        payload = json.load(request)
        handler = self.apis.get(payload['api'], self.api_not_found)
        del payload['api']
        try:
            response = {'error': None, 'result': handler(**payload)}
        except self.Error as e:
            response = {'error': e.args[0]}
        return HttpResponse(json.dumps(response).encode(), content_type='application/json')

    def api(self, f):
        self.apis[f.__name__] = f
        return f

    def api_not_found(self, *args, **kwargs):
        raise self.Error('api_not_found')
