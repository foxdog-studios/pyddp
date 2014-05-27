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

from ws4py.client.threadedclient import WebSocketClient

__all__ = ['ObservableWebSocketClient']


class ObservableWebSocketClient(WebSocketClient):
    def __init__(self, url):
        super(ObservableWebSocketClient, self).__init__(str(url))
        self._opened = []
        self._received_message = []
        self._closed = []

    def _call(self, listeners, *args, **kwargs):
        for listener in listeners:
            listener(*args, **kwargs)

    def _on(self, listeners, listener):
        listeners.append(listener)

    def _off(self, listeners, listener):
        listeners.remove(listener)

    def opened(self):
        self._call(self._opened)

    def on_opened(self, listener):
        self._on(self._opened, listener)

    def off_opened(self, listener):
        self._off(self._opened, listener)

    def received_message(self, message):
        self._call(self._received_message, message)

    def on_received_message(self, listener):
        self._on(self._received_message, listener)

    def off_received_message(self, listener):
        self._off(self._received_message, listener)

    def closed(self, code, reason=None):
        self._call(self._closed, code, reason=reason)

    def on_closed(self, listener):
        self._on(self._closed, listener)

    def off_closed(self, listener):
        self._off(self._closed, listener)

