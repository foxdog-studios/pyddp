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

from ddp.message.client.method_message_factory import MethodMessageFactory
from .future import Future
from .subscriber import Subscriber

__all__ = ['MethodCaller']


class MethodCaller(object):
    def __init__(self, board, ids):
        self._board = board
        self._ids = ids
        self._factory = MethodMessageFactory(ids)
        self._futures = {}
        self._subscriber = Subscriber(board, {
            ':message:received:result': self._on_result,
        })

    def _on_result(self, topic, result):
        if result.id in self._futures:
            future = self._futures[result.id]
            del self._futures[result.id]
            future.set(result)

    def call(self, method, params):
        message = self._factory.build(method, params)
        self._futures[message.id] = future = Future()
        self._board.publish(':message:send:method', message)
        return future

    def enable(self):
        self._subscriber.subscribe()

    def disable(self):
        self._subscriber.unsubscribe()

