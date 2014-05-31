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

import threading
import unittest

from ddp.pubsub.future import Future
from ddp.pubsub.timeout_error import TimeoutError


class FutureTestCase(unittest.TestCase):
    def test_set_and_get(self):
        condition = threading.Condition()
        future = Future(condition)
        original_result = 'result'
        def set_result():
            future.set(original_result)
        setter = threading.Thread(target=set_result)
        with condition:
            setter.start()
            self.assertFalse(future.has_result())
            result = future.get()
        self.assertTrue(future.has_result())
        self.assertEqual(result, original_result)

    def test_get_timeout(self):
        with self.assertRaises(TimeoutError):
            Future().get(timeout=0.001)

    @unittest.skip('Requires manually intervention')
    def test_get_interruptable(self):
        Future().get()

