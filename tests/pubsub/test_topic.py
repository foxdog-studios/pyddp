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

from ddp.pubsub.topic import Topic


class TopicTestCase(unittest.TestCase):
    def test_addition(self):
        a = Topic('a')
        self.assertEqual(a + 'b', Topic('b', parent=a))
        with self.assertRaises(TypeError):
            a + object()

    def test_equality_and_hash(self):
        a = Topic('a')
        ab = Topic('b', parent=a)
        abc1 = Topic('c', parent=ab)
        abc2 = Topic('c', parent=ab)
        abd = Topic('d', parent=ab)
        ac = Topic('c', parent=a)

        def assert_hash(t1, t2):
            self.assertEqual(hash(t1), hash(t2))

        # Check same object equality
        self.assertEqual(a, a)
        assert_hash(a, a)
        self.assertEqual(ab, ab)
        assert_hash(ab, ab)
        self.assertEqual(abc1, abc1)
        assert_hash(abc1, abc1)
        self.assertEqual(abc2, abc2)
        assert_hash(abc2, abc2)
        self.assertEqual(abd, abd)
        assert_hash(abd, abd)

        # Check same name and parent
        self.assertEqual(abc1, abc2)
        assert_hash(abc1, abc2)

        # Check same name and different parent
        self.assertNotEqual(abc1, ac)

        # Check different name and same parent
        self.assertNotEqual(abc1, abd)

        # Check different type
        self.assertNotEqual(abc1, object())

    def test_invalid_name(self):
        with self.assertRaises(TypeError):
            Topic(object())

    def test_invalid_parent(self):
        with self.assertRaises(TypeError):
            Topic('name', parent=object())

    def test_iter(self):
        a = Topic('a')
        ab = a + 'b'
        abc = ab + 'c'
        i1 = iter(abc)
        i2 = iter(abc)
        self.assertEqual(next(i1), abc)
        self.assertEqual(next(i2), abc)
        self.assertEqual(next(i1), ab)
        self.assertEqual(next(i2), ab)
        self.assertEqual(next(i1), a)
        self.assertEqual(next(i2), a)
        self.assertIsNone(next(i1))
        self.assertIsNone(next(i2))
        with self.assertRaises(StopIteration):
            next(i1)
        with self.assertRaises(StopIteration):
            next(i2)

    def test_parse(self):
        actual = Topic.parse('a:b:c')
        expected = Topic('c', parent=Topic('b', parent=Topic('a')))
        self.assertEqual(actual, expected)

    def test_repr(self):
        topic = Topic('a') + 'b' + 'c'
        self.assertEqual(eval(repr(topic)), topic)

    def test_str(self):
        self.assertEqual(str(Topic('a') + 'b' + 'c'), 'a:b:c')

