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

from .message import Message

__all__ = ['PongMessage']


class PongMessage(Message):
    def __init__(self, id=None):
        super(PongMessage, self).__init__()
        self._id = id

    def __eq__(self, other):
        return isinstance(other, PongMessage) and self._id == other._id

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'PongMessage(id={!r})'.format(self._id)

    @property
    def id(self):
        return self._id

    def has_id(self):
        return self._id is not None

