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

from ddp.message.server.result_message import ResultMessage


class ResultMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.id = 'test'
        self.result = {'result': [True, 1.0]}
        self.error = 'error'

    def test_equality(self):
        m1 = ResultMessage('a', result='result1')
        m2 = ResultMessage('a', result='result1')
        m3 = ResultMessage('a', result='result2')
        m4 = ResultMessage('b', result='result1')
        m5 = ResultMessage('a', error='error1')
        m6 = ResultMessage('a', error='error1')
        m7 = ResultMessage('a', error='error2')
        self.assertEqual(m1, m1)
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)
        self.assertNotEqual(m1, m4)
        self.assertNotEqual(m1, object())
        self.assertEqual(m5, m6)
        self.assertNotEqual(m5, m7)

    def test_with_result(self):
        message = ResultMessage(self.id, result=self.result)
        self.assertEqual(message.id, self.id)
        self.assertTrue(message.has_result())
        self.assertEqual(message.result, self.result)
        self.assertFalse(message.has_error())
        self.assertIsNone(message.error)

    def test_with_error(self):
        message = ResultMessage(self.id, error=self.error)
        self.assertEqual(message.id, self.id)
        self.assertFalse(message.has_result())
        self.assertIsNone(message.result)
        self.assertTrue(message.has_error())
        self.assertEqual(message.error, self.error)

