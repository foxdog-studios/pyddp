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

import threading

from .timeout import Timeout

__all__ = ['Future']


class Future(object):
    def __init__(self, condition=None, poll_interval=0.01):
        if condition is None:
            condition = threading.Condition()
        self._condition = condition
        self._has_result = False
        self._poll_interval = poll_interval
        self._result = None

    def _wait_result(self, get_timeout):
        with self._condition:
            while not self._has_result:
                self._condition.wait(get_timeout())

    def has_result(self):
        with self._condition:
            return self._has_result

    def get(self, timeout=None):
        # Always use a timeout (even when one is not passed) so that
        # this method is interruptible. However, if the timeout elapses
        # and a one was not passed, just keep looping. Polling isn't
        # ideal but that's threading in Python.
        if timeout is None:
            get_timeout = lambda: self._poll_interval
        else:
            get_timeout = Timeout(timeout).get_remaining

        self._wait_result(get_timeout)
        return self._result

    def set(self, result):
        assert not self._has_result
        with self._condition:
            self._result = result
            self._has_result = True
            self._condition.notify_all()

