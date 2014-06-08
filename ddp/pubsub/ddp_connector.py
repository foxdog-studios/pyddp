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

from ddp.messages.client.connect_message import ConnectMessage
from .subscriber import Subscriber
from .topics import (
    DDPConnected,
    MessageReceivedConnected,
    MessageSendConnect,
    SocketOpened,
)

__all__ = ['DDPConnector']


class DDPConnector(Subscriber):
    def __init__(self, board, session=None):
        super(DDPConnector, self).__init__(board, {
                SocketOpened: self._on_socket_opened,
                MessageReceivedConnected: self._on_ddp_connected})
        self._board = board
        self._session = session

    def _on_socket_opened(self, topic):
        self._board.publish(MessageSendConnect,
                            ConnectMessage('pre2', session=self._session))

    def _on_ddp_connected(self, topic, message):
        self._session = message.session
        self._board.publish(DDPConnected)

