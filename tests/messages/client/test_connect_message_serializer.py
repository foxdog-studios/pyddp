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
from ddp.messages.client.connect_message_serializer import (
        ConnectMessageSerializer)


class ConnectMessageSerializerTestCase(unittest.TestCase):
    def setUp(self):
        self.serializer = ConnectMessageSerializer()
        self.version = 'pre2'
        self.support = ['pre2', 'pre1']
        self.session = 'session'

    def test_with_support_with_session(self):
        message = ConnectMessage(self.version, support=self.support,
                                 session=self.session)
        pod = self.serializer.serialize(message)
        expected = {'msg': 'connect', 'version': self.version,
                    'support': self.support, 'session': self.session}
        self.assertEqual(pod, expected)

    def test_with_support_without_session(self):
        message = ConnectMessage(self.version, support=self.support)
        expected = {'msg': 'connect', 'version': self.version,
                    'support': self.support}
        pod = self.serializer.serialize(message)
        self.assertEqual(pod, expected)

    def test_without_support_with_session(self):
        message = ConnectMessage(self.version, session=self.session)
        expected = {'msg': 'connect', 'version': self.version,
                    'support': [self.version], 'session': self.session}
        pod = self.serializer.serialize(message)
        self.assertEqual(pod, expected)

    def test_without_support_without_session(self):
        message = ConnectMessage(self.version)
        pod = self.serializer.serialize(message)
        self.assertEqual(pod, {'msg': 'connect', 'version': self.version,
                               'support': [self.version]})

