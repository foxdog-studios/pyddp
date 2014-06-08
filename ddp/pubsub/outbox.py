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

from .subscriber import Subscriber
from .topics import DDPConnected, RawSend, SocketClosed

__all__ = ['Outbox']


class Outbox(Subscriber):
    def __init__(self, board):
        super(Outbox, self).__init__(board, {
            DDPConnected: self._on_connected,
            SocketClosed: self._on_closed,
        })
        self._board = board
        self._outbox = []
        self._raw_subscriber = Subscriber(board, {RawSend: self._on_send})

    def _on_connected(self, topic):
        self._raw_subscriber.unsubscribe()
        for raw in self._outbox:
            self._board.publish(RawSend, raw)
        self._outbox = []

    def _on_send(self, topic, raw):
        self._outbox.append(raw)

    def _on_closed(self, topic, was_clean, code, reason):
        self._raw_subscriber.subscribe()

    def subscribe(self):
        super(Outbox, self).subscribe()
        self._raw_subscriber.subscribe()

    def unsubscribe(self):
        self._raw_subscriber.unsubscribe()
        super(Outbox, self).unsubscribe()

