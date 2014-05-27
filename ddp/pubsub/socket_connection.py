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

from functools import wraps

from .subscriber import Subscriber

__all__ = ['SocketConnection']


class SocketConnection(object):
    def __init__(self, board, socket_factory):
        self._board = board
        self._socket = None
        self._socket_factory = socket_factory
        self._subscriber = Subscriber(board, {
            ':socket:connect': self._on_connect,
            ':socket:disconnect': self._on_disconnect,
            ':raw:send': self._on_send,
        })

    def _publish(self, topic, *args, **kwargs):
        self._board.publish(topic, *args, **kwargs)

    def _publish_error(func):
        @wraps(func)
        def wrapper(self, topic, *args, **kwargs):
            try:
                return func(self, topic, *args, **kwargs)
            except Exception as error:
                self._publish(':socket:error', error)
        return wrapper

    def _start_observing(self):
        self._socket.on_opened(self._on_opened)
        self._socket.on_received_message(self._on_received_message)
        self._socket.on_closed(self._on_closed)

    def _stop_observing(self):
        self._socket.off_closed(self._on_closed)
        self._socket.off_received_message(self._on_received_message)
        self._socket.off_opened(self._on_opened)

    # =====================================================================
    # = Publications                                                      =
    # =====================================================================

    def _on_opened(self):
        self._publish(':socket:connected')

    def _on_closed(self, code, reason=None):
        self._stop_observing()
        self._socket = None
        self._publish(':socket:disconnected', code, reason=reason)

    def _on_received_message(self, message):
        self._publish(':raw:received', unicode(message))


    # =====================================================================
    # = Subscriptions                                                     =
    # =====================================================================

    @_publish_error
    def _on_connect(self, topic):
        if self._socket is None:
            self._socket = self._socket_factory.build()
            self._start_observing()
            try:
                self._socket.connect()
            except:
                self._stop_observing()
                self._socket = None
                raise

    @_publish_error
    def _on_send(self, topic, raw):
        if self._socket is not None:
            self._socket.send(raw)

    @_publish_error
    def _on_disconnect(self, topic):
        if self._socket is not None:
            self._stop_observing()
            self._socket.close()
            self._socket = None


    # =====================================================================
    # = Controls                                                          =
    # =====================================================================

    def enable(self):
        self._subscriber.subscribe()

    def disable(self):
        self._subscriber.unsubscribe()
        if self._socket is not None:
            self._stop_observing()

