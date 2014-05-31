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

from copy import copy

from .server_message import ServerMessage

__all__ = ['ReadyMessage']


class ReadyMessage(ServerMessage):
    def __init__(self, subs):
        self._subs = copy(subs)

    def  __eq__(self, other):
        if isinstance(other, ReadyMessage):
            return self._subs == other._subs
        return super(ReadyMessage, self).__eq__(other)

    def __str__(self):
        return 'ReadyMessage({!r})'.format(self._subs)

    @property
    def subs(self):
        return copy(self._subs)

