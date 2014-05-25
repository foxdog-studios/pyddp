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

from ddp.messages.server_message import ServerMessage
from ddp.utils import exists

__all__ = ['ResultMessage']


class ResultMessage(ServerMessage):
    def __init__(self, id_, error=None, result=None):
        super(ResultMessage, self).__init__()

        # The spec says that either error or result must be given. But, the
        # given result could be None (e.g., the methods does not return
        # anything). So, the only meaningful check is that if error exists
        # then result must not exist.
        if exists(error) and exists(result):
            raise ValueError('error and result cannot both be given')

        self._id = id_
        self._error = error
        self._result = result

    def __eq__(self, other):
        return (self._id == other._id
                and self._error == other._error
                and self._result == other._result)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (
            'ResultMessage('
            'id_={!r}, '
            'error={!r}, '
            'result={!r})'
        ).format(
            self._id,
            self._error,
            self._result
        )

    @property
    def id_(self):
        return self._id

    @property
    def error(self):
        if not self.has_error():
            raise AttributeError('result message has no `error` field')
        return self._error

    @property
    def result(self):
        if not self.has_result():
            raise AttributeError('result message has not `result` field')
        return self._result

    def has_error(self):
        return exists(self._error)

    def has_result(self):
        return exists(self._result)



