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

import asyncio

from .subscriber import Subscriber
from .topics import SocketOpen, RawSend, SocketClose, SocketError

__all__ = ['SocketConnector']


class SocketConnector(Subscriber):
    def __init__(self, board, loop, websocket_client_factory):
        super(SocketConnector, self).__init__(
                board,
                {SocketOpen: self._on_open})
        self._loop = loop
        self._factory = websocket_client_factory

    def _on_open(self, topic):
        task = self._create_task(self._create_connection())
        task.add_done_callback(self._on_create_connection_done)

    def _create_connection(self):
        return self._loop.create_connection(
            self._factory,
            self._factory.host,
            self._factory.port)

    def _create_task(self, coro):
        return asyncio.Task(coro, loop=self._loop)

    def _on_create_connection_done(self, future):
        error = future.exception()
        if error is not None:
            self._board.publish(SocketError, error)

