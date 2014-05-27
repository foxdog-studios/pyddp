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

from .subscriber import Subscriber

__all__ = ['PodMessageFilter']


class PodMessageFilter(object):
    def __init__(self, board, pod_message_filter):
        self._board = board
        self._pod_message_filter = pod_message_filter
        self._subscriber = Subscriber(board, {
            ':pod:received': self._on_received,
        })

    def _on_received(self, topic, pod):
        if self._accept(pod):
            topic = ':pod:accepted:' + self._get_type(pod)
        else:
            topic = ':pod:rejected'
        self._board.publish(topic, pod)

    def _accept(self, pod):
        return self._pod_message_filter.accept(pod)

    def _get_type(self, pod):
        return self._pod_message_filter.get_type(pod)

    def enable(self):
        self._subscriber.subscribe()

    def disable(self):
        self._subscriber.unsubscribe()

