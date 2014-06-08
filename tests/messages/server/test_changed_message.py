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

from ddp.messages.server.changed_message import ChangedMessage


class ChangedMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.collection = 'collection'
        self.id = 'id'

    def test_without_cleared_without_fields(self):
        message = ChangedMessage(self.collection, self.id)
        self.assertEqual(message.collection, self.collection)
        self.assertEqual(message.id, self.id)
        self.assertFalse(message.has_cleared())
        self.assertIsNone(message.cleared)
        self.assertFalse(message.has_fields())
        self.assertIsNone(message.fields)

