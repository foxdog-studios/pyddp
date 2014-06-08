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

from ddp.messages.client.method_message import MethodMessage


class MethodMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.id1 = 'id1'
        self.id2 = 'id2'
        self.method = 'method'
        self.params = ['arg1', True, 1]
        self.m1 = MethodMessage(self.id1, self.method, self.params)
        self.m2 = MethodMessage(self.id1, self.method, self.params)
        self.m3 = MethodMessage(self.id2, self.method, self.params)

    def test_attributes(self):
        self.assertEqual(self.m1.id, self.id1)
        self.assertEqual(self.m1.method, self.method)
        self.assertEqual(self.m1.params, self.params)

    def test_equality(self):
        self.assertEqual(self.m1, self.m1)
        self.assertEqual(self.m1, self.m2)
        self.assertNotEqual(self.m1, self.m3)
        self.assertNotEqual(self.m1, object())

    def test_str(self):
        self.assertEqual(eval(str(self.m1)), self.m1)

