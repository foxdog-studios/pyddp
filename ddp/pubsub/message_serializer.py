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

__all__ = ['MessageSerializer']


class MessageSerializer(object):
    def __init__(self, board, serializer):
        self._board = board
        self._serializer = serializer
        self._subscriber = Subscriber(board, {
            ':message:send:' + self._get_message_type(): self._on_send,
        })

    def _get_message_type(self):
        return self._serializer.MESSAGE_TYPE

    def _on_send(self, topic, message):
        try:
            pod = self._serialize(message)
        except Exception as error:
            self._board.publish(
                ':message:error:' + self._get_message_type(),
                message,
                error,
            )
        else:
            self._board.publish(':pod:send:' + self._get_message_type(), pod)

    def _serialize(self, message):
        return self._serializer.serialize(message)

    def enable(self):
        self._subscriber.subscribe()

    def disable(self):
        self._subscriber.unsubscribe()

