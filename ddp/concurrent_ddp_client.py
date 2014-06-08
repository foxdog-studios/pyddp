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

from .utils import ensure_asyncio
ensure_asyncio()
import asyncio

from .ddp_client import DDPClient
from .pubsub.future import Future

__all__ = ['ConcurrentDDPClient']


class ConcurrentDDPClient(object):
    def __init__(self, url, debug=False):
        self._client = None
        self._condition = threading.Condition()
        self._loop = None
        self._ready = False
        self._thread = threading.Thread(
            target=self._run,
            name='DDPClient',
            args=(url, debug),
        )

    def _run(self, url, debug):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._client = DDPClient(self._loop, url, debug=debug)
        self._client.open()
        with self._condition:
            self._ready = True
            self._condition.notify_all()
        self._loop.run_forever()

    def start(self):
        with self._condition:
            self._thread.start()
            while not self._ready:
                self._condition.wait()

    def stop(self):
        self._loop.stop()

    def join(self):
        self._thread.join()
        self._loop.close()

    def call(self, method, *params):
        async_future = asyncio.Future(loop=self._loop)
        self._call_soon(self._client.call, async_future, method, *params)
        future = Future()
        def callback(async_future):
            future.set(async_future.result())
        async_future.add_done_callback(callback)
        return future

    def _call_soon(self, *args, **kwargs):
        return self._loop.call_soon_threadsafe(*args, **kwargs)

