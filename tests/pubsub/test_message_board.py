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

from ddp.pubsub.message_board import MessageBoard
from ddp.pubsub.topic import Topic

__all__ = ['MessageBoardTestCase']


class MessageBoardTestCase(unittest.TestCase):
    def setUp(self):
        self.called = False
        self.loop = asyncio.new_event_loop()

    def tearDown(self):
        self.loop.close()

    def test_subscribe(self):
        board = MessageBoard(self.loop)
        expected_topic = Topic.parse('a:b:c')
        expected_args = (1, 2, 3)
        expected_kwargs = {'kwarg': True}
        def subscriber(topic, *args, **kwargs):
            self.called = True
            self.assertEqual(topic, expected_topic)
            self.assertEqual(args, expected_args)
            self.assertEqual(kwargs, expected_kwargs)
            self.loop.stop()
        board.subscribe(expected_topic, subscriber)
        board.publish(expected_topic, *expected_args, **expected_kwargs)
        self.loop.run_forever()
        self.assertTrue(self.called)

