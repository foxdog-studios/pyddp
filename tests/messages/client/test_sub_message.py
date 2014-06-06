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

from ddp.messages.client.sub_message import SubMessage


class SubMessageTestCase(unittest.TestCase):
    def test_equality(self):
        m1 = SubMessage('id1', 'name1')
        m2 = SubMessage('id1', 'name1')
        m3 = SubMessage('id1', 'name1', params=['param'])
        m4 = SubMessage('id2', 'name1')
        m5 = SubMessage('id2', 'name2')
        self.assertEqual(m1, m1)
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)
        self.assertNotEqual(m1, m4)
        self.assertNotEqual(m4, m5)
        self.assertNotEqual(m1, object())

    def test_str(self):
        message = SubMessage('id', 'name', params=['param'])
        self.assertEqual(eval(str(message)), message)

    def test_with_params(self):
        id = 'id'
        name = 'name'
        params = [True, 1.0]
        message = SubMessage(id, name, params)
        self.assertEqual(message.id, id)
        self.assertEqual(message.name, name)
        self.assertTrue(message.has_params())
        self.assertEqual(message.params, params)

    def test_without_params(self):
        id = 'id'
        name = 'name'
        message = SubMessage(id, name)
        self.assertEqual(message.id, id)
        self.assertEqual(message.name, name)
        self.assertFalse(message.has_params())
        self.assertIsNone(message.params)

