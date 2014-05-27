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

__all__ = ['PodMessageParser']


class PodMessageParser(object):
    def __init__(self, board, parser):
        self._board = board
        self._parser = parser
        self._subscriber = Subscriber(board, {
            ':raw:received': self._on_received,
        })

    def _on_received(self, topic, raw):
        try:
            pod = self._parse(raw)
        except Exception as error:
            self._board.publish(':raw:error', raw, error)
        else:
            self._board.publish(':pod:received', pod)

    def _parse(self, raw):
        return self._parser.parse(raw)

    def enable(self):
        self._subscriber.subscribe()

    def disable(self):
        self._subscriber.unsubscribe()

