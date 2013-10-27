from ws4py.client.threadedclient import WebSocketClient


def callback(name):
    def callback(self, *args, **kwargs):
        return self._callback(name, *args, **kwargs)
    return callback


class StrategyWebSocketClient(WebSocketClient):
    def __init__(self, url, closed_callback=None, opened_callback=None,
                 received_message_callback=None):
        super(StrategyWebSocketClient, self).__init__(url)
        self._closed_callback = closed_callback
        self._opened_callback = opened_callback
        self._received_message_callback = received_message_callback

    def _callback(self, name, *args, **kwargs):
        callback = getattr(self, '_%s_callback' % (name,))
        if callback is None:
            return False
        callback(*args, **kwargs)
        return True

    closed = callback('closed')
    opened = callback('opened')
    received_message = callback('received_message')

