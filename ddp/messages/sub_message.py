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

from ddp.messages.client_message import ClientMessage

__all__ = ['SubMessage']


class SubMessage(ClientMessage):
    def __init__(self, id_, name, params=None):
        super(SubMessage, self).__init__()
        self._id = id_
        self._name = name
        self._params = copy(params)

    def __eq__(self, other):
        return (self._id == other._id
                and self._name == other._name
                and self._params == other._params)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (
            'SubMessage('
            'id_={!r}, '
            'name={!r}, '
            'params={!r})'
        ).format(
            self._id,
            self._name,
            self._params
        )

    @property
    def id_(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def params(self):
        if not self.has_params():
            raise AttributeError('sub message has no `params` field')
        return self._params

    def has_params(self):
        return self._params is not None

