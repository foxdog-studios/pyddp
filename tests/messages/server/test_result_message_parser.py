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

from ddp.messages.server.result_message import ResultMessage
from ddp.messages.server.result_message_parser import ResultMessageParser


class ResultMessageParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = ResultMessageParser()
        self.id = 'id'
        self.error = 'error'
        self.result = {'result': [True, 1.0]}

    def test_with_error(self):
        message = self.parser.parse({'msg': 'result', 'id': self.id,
                                     'error': self.error})
        self.assertEqual(message, ResultMessage(self.id, error=self.error))

    def test_with_result(self):
        message = self.parser.parse({'msg': 'result', 'id': self.id,
                                     'result': self.result})
        self.assertEqual(message, ResultMessage(self.id, result=self.result))

    def test_with_error_with_result(self):
        with self.assertRaises(ValueError):
            self.parser.parse({'msg': 'result', 'id': self.id,
                               'error': self.error, 'result': self.result})

    def test_without_error_without_reuslt(self):
        message = self.parser.parse({'msg': 'result', 'id': self.id})
        self.assertEqual(message, ResultMessage(self.id))

