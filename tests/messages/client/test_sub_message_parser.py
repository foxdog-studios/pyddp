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
from ddp.messages.client.sub_message_parser import SubMessageParser


__all__ = ['SubMessageParserTestCase']


class SubMessageParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = SubMessageParser()
        self.id = 'id'
        self.name = 'name'
        self.params = ['param1', True, 1.0]

    def _make_pod(self, **kwargs):
        pod = {'msg': 'sub', 'id': self.id, 'name': self.name}
        pod.update(kwargs)
        return pod

    def _make_message(self, **kwargs):
        return SubMessage(self.id, self.name, **kwargs)

    def test_with_params(self):
        kwargs = {'params': self.params}
        message = self.parser.parse(self._make_pod(**kwargs))
        self.assertEqual(message, self._make_message(**kwargs))

    def test_without_params(self):
        message = self.parser.parse(self._make_pod())
        self.assertEqual(message, self._make_message())

