from ws4py.client.threadedclient import WebSocketClient
from ws4py.messaging import Message


# Monkey patch Python 2 / 3 compatibility issue
def __str__(self):
    return self.data.decode(self.encoding)

Message.__str__ =  __str__


def callback(name):
    def callback(self, *args, **kwargs):
        return self._callback(name, *args, **kwargs)
    return callback


class StrategyWebSocketClient(WebSocketClient):
    def __init__(self, url, closed_callback=None, opened_callback=None,
                 received_message_callback=None):
        super().__init__(url)
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

