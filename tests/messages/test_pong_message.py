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

from ddp.messages.pong_message import PongMessage


class PongMessageTestCase(unittest.TestCase):
    def test_equality(self):
        m1 = PongMessage()
        m2 = PongMessage()
        m3 = PongMessage(id='m3')
        m4 = PongMessage(id='m4')
        self.assertEqual(m1, m1)
        self.assertEqual(m1, m2)
        self.assertEqual(m3, m3)
        self.assertNotEqual(m1, m3)
        self.assertNotEqual(m3, m4)
        self.assertNotEqual(m1, object())
        self.assertNotEqual(m3, object())

    def test_str(self):
        m1 = PongMessage()
        m2 = PongMessage(id='m2')
        self.assertEqual(eval(str(m1)), m1)
        self.assertEqual(eval(str(m2)), m2)

    def test_with_id(self):
        id = 'test'
        message = PongMessage(id=id)
        self.assertTrue(message.has_id())
        self.assertEqual(message.id, id)

    def test_without_id(self):
        message = PongMessage()
        self.assertFalse(message.has_id())
        self.assertIsNone(message.id)

