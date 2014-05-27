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

__all__ = ['ErrorMessage']


class ErrorMessage(ServerMessage):
    def __init__(self, reason, offending_pod):
        self._reason = reason
        self._offending_pod = offending_pod

    def __eq__(self, other):
        return isinstance(other, ErrorMessage) \
                and self._reason == other._reason \
                and self._offending_pod == other._offending_pod

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (
            'ErrorMessage('
            'reason={!r}, '
            'offending_pod={!r})'
        ).format(
            self._reason,
            self._offending_pod
        )

    @property
    def reason(self):
        return self._reason

    @property
    def offending_pod(self):
        return self._offending_pod

