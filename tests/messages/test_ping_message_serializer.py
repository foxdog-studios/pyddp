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
from ddp.messages.ping_message_serializer import PingMessageSerializer


class PingMessageSerializerTestCase(unittest.TestCase):
    def setUp(self):
        self.serializer = PingMessageSerializer()

    def test_serialize_with_id(self):
        id = 'test'
        pod = self.serializer.serialize(PingMessage(id=id))
        self.assertEqual(pod, {'msg': 'ping', 'id': id})

    def test_serialize_without_id(self):
        pod = self.serializer.serialize(PingMessage())
        self.assertEqual(pod, {'msg': 'ping'})

