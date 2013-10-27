import json


def union(*dicts):
    u = {}
    for dict_ in dicts:
        for key, value in dict_.items():
            if key in u:
                raise ValueError('more than one value for %r' % (key,))
            u[key] = value
    return u


class Request(object):
    def __init__(self, msg, params):
        self._msg = msg
        self._params = params

    def __str__(self):
        request_params = union({'msg': self._msg}, self._params)
        return json.dumps(request_params)


class ConnectRequest(Request):
    def __init__(self, version, support, session=None):
        request_params = {'version': version, 'support': support}
        if session is not None:
            request_params['session'] = session
        super(ConnectRequest, self).__init__('connect', request_params)


class MethodRequest(Request):
    def __init__(self, id_, method, params):
        request_params = {'id': id_, 'method': method, 'params': params}
        super(MethodRequest, self).__init__('method', request_params)

