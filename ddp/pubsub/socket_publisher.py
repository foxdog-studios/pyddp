# -*- coding: utf-8 -*-

# Copyright 2014 Foxdog Studios
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ddp.utils import ensure_asyncio
ensure_asyncio()

from autobahn.asyncio.websocket import WebSocketClientProtocol

from .subscriber import Subscriber
from .topics import (RawReceived, RawSend, SocketClose, SocketClosed,
                     SocketOpened)

__all__ = ['SocketPublisher']


class SocketPublisher(WebSocketClientProtocol):
    def __init__(self, board):
        super(SocketPublisher, self).__init__()
        self._board = board
        self._close_subscriber = Subscriber(board, {
                SocketClose: self._on_close})
        self._close_subscriber.subscribe()
        self._send_subscriber = Subscriber(board, {
                RawSend: self._on_send})

    def _on_send(self, topic, raw):
        self.sendMessage(raw)

    def _on_close(self, topic):
        self.sendClose()

    def _publish(self, topic, *args, **kwargs):
        self._board.publish(topic, *args, **kwargs)

    def onOpen(self):
        self._send_subscriber.subscribe()
        self._publish(SocketOpened)

    def onMessage(self, payload, isBinary):
        self._publish(RawReceived, payload)

    def onClose(self, wasClean, code, reason):
        self._send_subscriber.unsubscribe()
        self._publish(SocketClosed, wasClean, code, reason)

