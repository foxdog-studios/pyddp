from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import threading
import unittest

from ddp.client import DdpClient
from ddp.future import Future, CompositeFuture
from ddp.messages import *


class FuturTestCase(unittest.TestCase):
    def test_callback(self):
        f1 = Future()
        callback_arg = [None]
        def callback(result):
            callback_arg[0] = result
        f1.add_callback(callback)
        result = 'Hello, World!'
        f1.set(result)
        self.assertEqual(callback_arg[0], result)

    def test_composite_get(self):
        f1 = Future()
        f2 = Future()
        cf = CompositeFuture([f1, f2])
        self.assertFalse(cf)
        self.assertEqual(cf[0], f1)
        self.assertEqual(cf[1], f2)
        r1 = 'a'
        f1.set(r1)
        self.assertFalse(cf)
        r2 = 'b'
        f2.set(r2)
        self.assertTrue(cf)
        self.assertEqual(cf.get(), [r1, r2])

    def test_get(self):
        future = Future()
        value = 'Hello, World!'
        t = threading.Thread(target=future.set, args=[value])
        t.start()
        self.assertEqual(future.get(), value)
        t.join()

    def test_timeout(self):
        future = Future()
        with self.assertRaises(RuntimeError):
            future.get(timeout=0.01)


class DdpClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = DdpClient('127.0.0.1:3000')

    def tearDown(self):
        self.client.disconnect()

    def test_connect(self):
        server_id, connected = self.client.connect()

    def test_connect_async(self):
        self.client.connect_async().get()

    def test_method(self):
        self.client.connect()
        arg = 'Hello, World!'
        result = self.client.method('echo', [arg])
        self.assertEqual(result['result'], arg)

    def test_method_sync(self):
        self.client.connect()
        arg = 'Hello, World!'
        result = self.client.method_async('echo', [arg])
        self.assertEqual(result.get()['result'], arg)


class MessagesTestCase(unittest.TestCase):
    def test_method_request(self):
        req = MethodRequest(1, 'echo', ['Hello, World!'])


if __name__ == '__main__':
    unittest.main()

