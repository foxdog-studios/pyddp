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

from ddp.messages.ping_message import PingMessage
from ddp.messages.message_serializer import MessageSerializer

__all__ = ['MessageSerializerTestCase']


class MessageSerializerTestCase(unittest.TestCase):
    def test_not_implemeted(self):
        with self.assertRaises(NotImplementedError):
            MessageSerializer().serialize_fields(PingMessage())

    def test_optimize(self):
        class MockMessage(object):
            def __init__(self, optimized=False):
                self.optimized = optimized
            def optimize(self):
                return MockMessage(optimized=True)
        class MockMessageSerializer(MessageSerializer):
            MESSAGE_TYPE = 'mock'
            def serialize_fields(self, message):
                return {'optimized': message.optimized}
        s1 = MockMessageSerializer()
        s2 = MockMessageSerializer(optimize=True)
        self.assertFalse(s1.serialize(MockMessage())['optimized'])
        self.assertTrue(s2.serialize(MockMessage())['optimized'])

