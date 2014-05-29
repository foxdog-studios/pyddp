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

__all__ = ['MessageBoard']


class MessageBoard(object):
    def __init__(self):
        self._lock = threading.RLock()
        self._pending = []
        self._publishing = False
        self._sep = ':'
        self._subscribers = {}

    def _publish(self):
        self._publishing = True
        while self._pending:
            topic_parts = []
            subscribers = dict(self._subscribers)
            topic, args, kwargs = self._pending.pop(0)
            for topic_part in topic.split(self._sep):
                topic_parts.append(topic_part)
                ancestor_topic = self._sep.join(topic_parts)
                if ancestor_topic in subscribers:
                    for subscriber in subscribers[ancestor_topic]:
                        subscriber(topic, *args, **kwargs)
        self._publishing = False

    def subscribe(self, topic, subscriber):
        with self._lock:
            self._subscribers.setdefault(topic, []).append(subscriber)

    def unsubscribe(self, topic, subscriber):
        with self._lock:
            has_subscribers = topic in self._subscribers
            if has_subscribers and subscriber in self._subscribers[topic]:
                self._subscribers[topic].remove(subscriber)
                if not self._subscribers[topic]:
                    del self._subscribers[topic]

    def publish(self, topic, *args, **kwargs):
        with self._lock:
            self._pending.append((topic, args, kwargs))
            if not self._publishing:
                self._publish()

