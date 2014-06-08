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
from .topics import SocketClosed, SocketError, SocketOpen

__all__ = ['SocketReconnector']


class SocketReconnector(Subscriber):
    def __init__(self, board):
        super(SocketReconnector, self).__init__( board, {
                SocketClosed: self._on_close,
                SocketError: self._on_error})
        self._board = board

    def _on_close(self, topic, was_clean, code, reason):
        self._publish_socket_open()

    def _on_error(self, topic, error):
        self._publish_socket_open()

    def _publish_socket_open(self):
        self._board.publish(SocketOpen)

