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

__all__ = ['Future']


class Future(object):
    def __init__(self):
        self._condition = threading.Condition()
        self._has_result = False
        self._result = None

    def has_result(self):
        with self._condition:
            return self._has_result

    def get(self, timeout=None):
        with self._condition:
            while not self._has_result:
                self._condition.wait(timeout)
        return self._result

    def set(self, result):
        assert not self._has_result
        with self._condition:
            self._result = result
            self._has_result = True
            self._condition.notify_all()

