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

from .client_message import ClientMessage

__all__ = ["ConnectMessage"]


class ConnectMessage(ClientMessage):
    def __init__(self, version, support=None, session=None):
        super(ConnectMessage, self).__init__()
        self._version = version
        self._support = copy(support)
        self._session = session

    def __eq__(self, other):
        return isinstance(other, ConnectMessage) \
                and self._version == other._version \
                and self._support == other._support \
                and self._session == other._session

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (
            'ConnectMessage('
            'version={!r}, '
            'support={!r}, '
            'session={!r})'
        ).format(
            self._version,
            self._support,
            self._session,
        )

    @property
    def version(self):
        return self._version

    @property
    def support(self):
        return copy(self._support)

    @property
    def session(self):
        return self._session

    def has_support(self):
        return self._support is not None

    def has_session(self):
        return self._session is not None

    def optimize(self):
        support = self._support

        if support is not None:
            support = copy(support)

            # It appears that the preferred version does not need to be
            # in the list of supported version.
            if self._version in support:
                support.remove(self._version)

            # Also, it appears that support can be omitted if empty.
            if not support:
                support = None

        optimized = type(self)(self._version, support=support,
                               session=self._session)

        return super(ConnectMessage, optimized).optimize()

