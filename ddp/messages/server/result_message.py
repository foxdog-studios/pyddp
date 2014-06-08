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

__all__ = ['ResultMessage']


class ResultMessage(ServerMessage):
    '''The result of a method call, either the return value or an error.

    Either ``error`` or ``result`` may be passed (possibly neither, but not
    both.. ``error`` and ``result`` are considered passed even if their value
    is ``None``.

    :param id: The ID passed with the method call.
    :type id: basestring
    :param error: An error thrown by the method or a method-not-found error.
    :type error: ddp.message.server.error
    :param result: The return value of the method, if any.
    '''

    def __init__(self, id, **kwargs):
        super(ResultMessage, self).__init__()

        # Check that either error and result has been passed.
        if kwargs.keys() not in [[], ['error'], ['result']]:
            raise ValueError('Either error or result may be passed, but not '
                             'both.')

        if not isinstance(id, basestring):
            raise ValueError('id must be an instance of basestring.')

        self._id = id

        self._has_error = 'error' in kwargs
        self._error = kwargs.get('error')

        self._has_result = 'result' in kwargs
        self._result = kwargs.get('result')

    def __eq__(self, other):
        if isinstance(other, ResultMessage):
            return (self._id == other._id
                    and self._has_error == other._has_error
                    and self._error == other._error
                    and self._has_result == other._has_result
                    and self._result == other._result)
        return super(ResultMessage, self).__eq__(other)

    def __str__(self):
        parts = ['ResultMessage(', repr(self._id)]
        if self._has_error:
            parts += [', error=', repr(self._error)]
        if self._has_result:
            parts += [', result=', repr(self._result)]
        parts.append(')')
        return ''.join(parts)

    @property
    def id(self):
        return self._id

    @property
    def error(self):
        return self._error

    @property
    def result(self):
        return self._result

    def has_error(self):
        '''Does the result carry an error?

        :retruns: True if the result carries an error and False otherwise.
        :rtype: bool
        '''
        return self._has_error

    def has_result(self):
        '''Does the result carry a return value?

        :returns: True if the result carries a return value and False
                  otherwise.
        :rtype: bool
        '''
        return self._has_result

