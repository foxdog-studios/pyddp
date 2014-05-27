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

__all__ = ['Logger']


class Logger(object):
    def __init__(self, board):
        self._subscriber = Subscriber(board, {'': self._on_publish})

    def _on_publish(self, topic, *args, **kwargs):
        lines = [topic]
        if args:
            lines.append('  Arguments:')
            for i, arg in enumerate(args):
                lines.append('    {}) {}'.format(i, arg))
        if kwargs:
            lines.append('  Keyword arguments:')
            for key, value in sorted(kwargs.items()):
                lines.append('    {} -> {}'.format(key, value))
        print('\n'.join(lines))

    def enable(self):
        self._subscriber.subscribe()

    def disable(self):
        self._subscriber.unsubscribe()

