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


__all__ = ['RootTopic', 'Topic']


RootTopic = None


class Topic(object):
    def __init__(self, name, parent=RootTopic):
        # Validate name
        if not isinstance(name, basestring):
            message = 'name must be an instance of basestring, not {}'
            raise TypeError(message.format(type(name)))

        # Validate parent
        if parent != RootTopic and not isinstance(parent, Topic):
            message = 'parent must be an instance of Topic, not {}'
            raise TypeError(message.format(type(parent)))

        super(Topic, self).__init__()
        self._name = name
        self._parent = parent

    def __eq__(self, other):
        if isinstance(other, Topic):
            return self._name == other._name and self._parent == other._parent
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __add__(self, child_name):
        if isinstance(child_name, basestring):
            return Topic(child_name, parent=self)
        return NotImplemented

    def __hash__(self):
        return hash(self._name) ^ hash(self._parent)

    def __iter__(self):
        topic = self
        while True:
            yield topic
            if topic == RootTopic:
                break
            topic = topic._parent

    def __repr__(self):
        parts = ['Topic(', repr(self._name)]
        if self._parent != RootTopic:
            parts += [', parent=', repr(self._parent)]
        parts.append(')')
        return ''.join(parts)

    def __str__(self):
        parts = []
        if self._parent != RootTopic:
            parts.append(str(self._parent))
        parts.append(self._name)
        return ':'.join(parts)

    @classmethod
    def parse(cls, full_name, sep=':'):
        topic = RootTopic
        for name in full_name.split(sep):
            topic = Topic(name, parent=topic)
        return topic

