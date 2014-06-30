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

from ddp.utils import default
from .client_message import ClientMessage


__all__ = ['ConnectMessage']


class ConnectMessage(ClientMessage):
    def __init__(self, version, support=None, session=None):
        super(ConnectMessage, self).__init__()
        self._version = version
        self._support = default(support, [version])
        self._session = session

        if self._version not in self._support:
            raise ValueError('support must contain version')

    def __eq__(self, other):
        if isinstance(other, ConnectMessage):
            return (self._version == other._version
                    and self._support == other._support
                    and self._session == other._session)
        return super(ConnectMessage, self).__eq__(other)

    def __str__(self):
        return 'ConnectMessage({!r}, support={!r}, session={!r})'.format(
                self._version,
                self._support,
                self._session)

    @property
    def version(self):
        return self._version

    @property
    def support(self):
        return copy(self._support)

    @property
    def session(self):
        return self._session

    def has_session(self):
        return self._session is not None

