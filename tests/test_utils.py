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

from ddp.utils import default


class DefaultTestCase(unittest.TestCase):
    def setUp(self):
        self.obj = 'obj'
        self.value = 'value'
        self.factory_value = 'factory_value'
        self.factory = lambda: self.factory_value

    def test_given_object_given_value(self):
        self.assertEqual(default(self.obj, value=self.value), self.obj)

    def test_given_object_given_factory(self):
        self.assertEqual(default(self.obj, factory=self.factory), self.obj)

    def test_given_value(self):
        self.assertEqual(default(None, value=self.value), self.value)

    def test_given_factory(self):
        self.assertEqual(default(None, factory=self.factory),
                         self.factory_value)

    def test_given_value_given_factory(self):
        with self.assertRaises(ValueError):
            default(None, value=self.value, factory=self.factory)

    def test_given_object_given_value_given_factory(self):
        with self.assertRaises(ValueError):
            default(self.obj, value=self.value, factory=self.factory)

