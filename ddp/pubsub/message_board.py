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

from functools import partial

__all__ = ['MessageBoard']


class MessageBoard(object):
    def __init__(self, loop):
        super(MessageBoard, self).__init__()
        self._loop = loop
        self._subscribers = {}

    def _call_subscribers(self, topic, *args, **kwargs):
        for ancestor_topic in topic:
            if ancestor_topic in self._subscribers:
                for subscriber in self._subscribers[ancestor_topic]:
                    subscriber(topic, *args, **kwargs)

    def publish(self, topic, *args, **kwargs):
        self._loop.call_soon(partial(self._call_subscribers, topic, *args,
                                     **kwargs))

    def subscribe(self, topic, subscriber):
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(subscriber)

    def unsubscribe(self, topic, subscriber):
        has_subscribers = topic in self._subscribers
        if has_subscribers and subscriber in self._subscribers[topic]:
            self._subscribers[topic].remove(subscriber)
            if not self._subscribers[topic]:
                del self._subscribers[topic]

