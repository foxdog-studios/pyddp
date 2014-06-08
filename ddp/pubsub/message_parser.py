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
from .topics import MessageReceived, PodAccepted

__all__ = ['MessageParser']


class MessageParser(Subscriber):
    def __init__(self, board, parser):
        super(MessageParser, self).__init__(board, {
                PodAccepted + parser.MESSAGE_TYPE: self._on_accepted})
        self._board = board
        self._parser = parser

    def _on_accepted(self, topic, pod):
        self._board.publish(MessageReceived + self._parser.MESSAGE_TYPE,
                            self._parser.parse(pod))

