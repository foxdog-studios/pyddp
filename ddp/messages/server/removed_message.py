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

from .server_message import ServerMessage

__all__ = ['RemovedMessage']


class RemovedMessage(ServerMessage):
    def __init__(self, collection, id):
        super(RemovedMessage, self).__init__()
        self._collection = collection
        self._id = id

    def __eq__(self, other):
        if isinstance(other, RemovedMessage):
            return (self._collection == other._collection
                    and self._id == other._id)
        return super(RemovedMessage, self).__eq__(other)

    def __str__(self):
        return 'RemovedMessage({!r}, {!r})'.format(self._collection, self._id)

    @property
    def collection(self):
        return self._collection

    @property
    def id(self):
        return self._id

