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

import imp
import sys


__all__ = ['default', 'ensure_asyncio']


def default(obj, value=None, factory=None):
    def raise_error():
        raise ValueType('value or factory must be given')
    if obj is None:
        if value is None:
            if factory is None:
                raise_error()
            return factory()
        if factory is not None:
            raise_error()
        return value
    return obj


def ensure_asyncio():
    try:
        import asyncio
    except ImportError:
        file, pathname, description = imp.find_module('trollius')
        try:
            asyncio = imp.load_module('asyncio', file, pathname, description)
        finally:
            if file is not None:
                try:
                    file.close()
                except:
                    pass
        sys.modules['asyncio'] = asyncio

