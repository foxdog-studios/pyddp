from itertools import count
from urllib.parse import urlunparse
import json
import threading
import time

from ddp.future import CompositeFuture, Future
from ddp.messages import *
from ddp.timeout import wrap_timeout
from ddp.websocket import StrategyWebSocketClient


DDP_VERSIONS = ['pre1']


class DdpClient:
    SCHEME = 'ws'
    URL = '/websocket'

    def __init__(self, host):
        self._id_counter = count()
        self._is_connected = False
        self._awaiting_reply = {}

        self._socket = StrategyWebSocketClient(
            self._build_url(host),
            closed_callback=self._closed_callback,
            opened_callback=self._opened_callback,
            received_message_callback=self._received_message_callback,
        )

    def _build_url(self, host):
        return urlunparse((self.SCHEME, host, self.URL, '', '', ''))

    def _send(self, request):
        self._socket.send(str(request))

    def _closed_callback(self, code, reason=None):
        pass

    def _opened_callback(self):
        self._send(ConnectRequest(DDP_VERSIONS[0], DDP_VERSIONS))

    def _received_message_callback(self, raw_message):
        message = json.loads(str(raw_message))
        if 'server_id' in message:
            handler = self._handle_server_id
        elif message.get('msg', None) == 'connected':
            handler = self._handle_connected
        elif 'id' in message:
            handler = self._handle_message_with_id
        else:
            handler = lambda message: None
        handler(message)

    def _handle_server_id(self, message):
        self._awaiting_reply.pop('server_id').set(message)

    def _handle_connected(self, message):
        self._awaiting_reply.pop('connected').set(message)

    def _handle_message_with_id(self, message):
        id_ = int(message['id'])
        if id_ in self._awaiting_reply:
            future = self._awaiting_reply.pop(id_)
            future.set(message)

    def connect(self, timeout=None):
        connected = self.connect_async()
        return connected.get(timeout=timeout)

    def connect_async(self):
        server_id = Future()
        connected = Future()
        self._awaiting_reply['server_id'] = server_id
        self._awaiting_reply['connected'] = connected
        self._socket.connect()
        return CompositeFuture([server_id, connected])

    def disconnect(self):
        self._socket.close()

    def method(self, method, params, timeout=None):
        return self.method_async(method, params).get(timeout=timeout)

    def method_async(self, method, params):
        id_ = next(self._id_counter)
        result = Future()
        self._awaiting_reply[id_] = result
        self._send(MethodRequest(str(id_), method, params))
        return result

