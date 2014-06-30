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

from ddp.messages.client.connect_message import ConnectMessage


class ConnectMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.version = 'pre2'
        self.session = 'session'
        self.support = ['pre2', 'pre1']
        self.support_optimized = ['pre1']

    def test_equality(self):
        m1 = ConnectMessage(self.version, support=self.support, session='a')
        m2 = ConnectMessage(self.version, support=self.support, session='a')
        m3 = ConnectMessage(self.version, support=self.support, session='b')
        self.assertEqual(m1, m1)
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)
        self.assertNotEqual(m1, object())

    def test_invalid_support(self):
        with self.assertRaises(ValueError):
            ConnectMessage(self.version, support=[])

    def test_str(self):
        m1 = ConnectMessage(self.version, support=self.support,
                            session=self.session)
        m2 = eval(str(m1))
        self.assertEqual(m1, m2)

    def test_repr(self):
        m1 = ConnectMessage(self.version, support=self.support,
                            session=self.session)
        m2 = eval(repr(m1))
        self.assertEqual(m1, m2)

    def test_with_support_with_session(self):
        message = ConnectMessage(self.version, support=self.support,
                                 session=self.session)
        self.assertEqual(message.version, self.version)
        self.assertEqual(message.support, self.support)
        self.assertTrue(message.has_session())
        self.assertEqual(message.session, self.session)

    def test_with_support_without_session(self):
        message = ConnectMessage(self.version, support=self.support)
        self.assertEqual(message.version, self.version)
        self.assertEqual(message.support, self.support)
        self.assertFalse(message.has_session())
        self.assertIsNone(message.session)

    def test_without_support_with_session(self):
        message = ConnectMessage(self.version, session=self.session)
        self.assertEqual(message.version, self.version)
        self.assertEqual(message.support, [self.version])
        self.assertTrue(message.has_session())
        self.assertEqual(message.session, self.session)

    def test_without_support_without_session(self):
        message = ConnectMessage(self.version)
        self.assertEqual(message.version, self.version)
        self.assertEqual(message.support, [self.version])
        self.assertFalse(message.has_session())
        self.assertIsNone(message.session)

