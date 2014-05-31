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

__all__ = ['UpdatedMessage']


class UpdatedMessage(ServerMessage):
    def __init__(self, methods):
        super(UpdatedMessage, self).__init__()
        self._methods = copy(methods)

    def __eq__(self, other):
        if isinstance(other, UpdatedMessage):
            return self._methods == other._methods
        return super(UpdatedMessage, self).__eq__(other)

    def __str__(self):
        return 'UpdatedMessage({!r})'.format(self._methods)

    @property
    def methods(self):
        return copy(self._methods)

