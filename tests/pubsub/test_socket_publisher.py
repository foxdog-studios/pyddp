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

import unittest

from ddp.utils import ensure_asyncio
ensure_asyncio()

import asyncio

from autobahn.asyncio.websocket import WebSocketClientFactory

from ddp.pubsub.message_board import MessageBoard
from ddp.pubsub.socket_publisher_factory import SocketPublisherFactory

__all__ = ['ProtocolTestCase']


class ProtocolTestCase(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.board = MessageBoard(self.loop)
        self.protocol = SocketPublisherFactory(self.board)

    def tearDown(self):
        self.loop.close()

    @unittest.skip
    def test(self):
        factory = WebSocketClientFactory(url='ws://127.0.0.1:29757/websocket')
        factory.protocol = self.protocol
        coro = self.loop.create_connection(factory, '127.0.0.1', 29757)
        self.loop.run_until_complete(coro)
        self.loop.run_forever()

