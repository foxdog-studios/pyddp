from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import threading
import unittest

from ddp import *


class AbstractMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.pod_factory = self.POD_FACTORY_CLASS()
        self.serializer = PodMessageSerializer()
        self.parser = PodMessageParser()
        self.pod_filter = self.POD_MESSAGE_FILTER_CLASS()
        self.msg_factory = self.MESSAGE_FACTORY_CLASS()

    def create_pod(self, message):
        return self.pod_factory.create(message)

    def serialize(self, pod):
        return self.serializer.serialize(pod)

    def parse(self, text):
        return self.parser.parse(text)

    def accept(self, pod):
        return self.pod_filter.accept(pod)

    def create_message(self, pod):
        return self.msg_factory.create(pod)

    def round_trip(self, msg1):
        pod1 = self.create_pod(msg1)
        text = self.serialize(pod1)
        pod2 = self.parse(text)
        self.assertTrue(self.accept(pod2))
        msg2 = self.create_message(pod2)
        return msg2

    def check_round_trip(self, msg1):
        msg2 = self.round_trip(msg1)
        self.assertEqual(msg1, msg2)


class ClientMessagesTestCase(AbstractMessageTestCase):
    MESSAGE_FACTORY_CLASS = ClientMessageFactory
    POD_FACTORY_CLASS = PodClientMessageFactory
    POD_MESSAGE_FILTER_CLASS = PodClientMessageFilter

    def test_connect(self):
        msg = ConnectMessage('pre1', session='session', support=['pre1'])
        self.check_round_trip(msg)

    def test_method(self):
        msg = MethodMessage('id', 'method', ['arg1', 'arg2', 'arg3'])
        self.check_round_trip(msg)

    def test_ping(self):
        msg = PingMessage(id_='id')
        self.check_round_trip(msg)

    def test_pong(self):
        msg = PongMessage(id_='id')
        self.check_round_trip(msg)

    def test_sub(self):
        msg = SubMessage('id', 'name', params=['arg1', 'arg2', 'arg3'])
        self.check_round_trip(msg)

    def test_unsub(self):
        msg = UnsubMessage('id')
        self.check_round_trip(msg)


class ServerMessagesTestCase(AbstractMessageTestCase):
    MESSAGE_FACTORY_CLASS = ServerMessageFactory
    POD_FACTORY_CLASS = PodServerMessageFactroy
    POD_MESSAGE_FILTER_CLASS = PodServerMessageFilter

    def test_added(self):
        msg = AddedMessage('collection', 'id',
                           fields=['field1', 'field2', 'field3'])
        self.check_round_trip(msg)

    def test_added_before(self):
        msg = AddedBeforeMessage('collection', 'id', 'before_id',
                                 fields=['field1', 'field2', 'field3'])
        self.check_round_trip(msg)

    def test_changed(self):
        msg = ChangedMessage('collection', 'id',
                             cleared=['field1', 'field2', 'field3'],
                             fields=['field1', 'field2', 'field3'])
        self.check_round_trip(msg)

    def test_connected(self):
        msg = ConnectedMessage('session')
        self.check_round_trip(msg)

    def test_error(self):
        msg = ErrorMessage('reason', {'field': 'value'})
        self.check_round_trip(msg)

    def test_failed(self):
        msg = FailedMessage('version')
        self.check_round_trip(msg)

    def test_moved_before(self):
        msg = MovedBeforeMessage('collection', 'id', 'id_before')
        self.check_round_trip(msg)

    def test_ping(self):
        msg = PingMessage(id_='id')
        self.check_round_trip(msg)

    def test_pong(self):
        msg = PongMessage(id_='id')
        self.check_round_trip(msg)

    def test_nosub(self):
        msg = NosubMessage('id', error='error')
        self.check_round_trip(msg)

    def test_ready(self):
        msg = ReadyMessage(['sub1', 'sub2', 'sub3'])
        self.check_round_trip(msg)

    def test_removed(self):
        msg = RemovedMessage('collection', 'id')
        self.check_round_trip(msg)

    def test_result(self):
        msg1 = ResultMessage('id', error='error')
        self.check_round_trip(msg1)
        msg2 = ResultMessage('id', result='result')
        self.check_round_trip(msg2)

        # Happens when a method does not return anything.
        msg3 = ResultMessage('id', result=None)
        self.check_round_trip(msg3)

    def test_updated(self):
        msg = UpdatedMessage(['method1', 'method2', 'method3'])
        self.check_round_trip(msg)


class SocketTestCase(unittest.TestCase):
    def setUp(self):
        self.url = str(ServerUrl('127.0.0.1:3000'))
        self.received = False
        self.disconnected = False

    def tearDown(self):
        del self.received
        del self.disconnected

    def test_ddp_connection(self):
        call_id = 'call_id'
        received_cond = threading.Condition()
        def received_message_callback(message):
            if isinstance(message, ResultMessage) and message.id_ == call_id:
                with received_cond:
                    self.received = True
                    received_cond.notify()

        disconnected_cond = threading.Condition()
        def disconnected_callback(code, reason=None):
            with disconnected_cond:
                self.disconnected = True
                disconnected_cond.notify()

        conn = DdpConnection(
            self.url,
            received_message_callback=received_message_callback,
            disconnected_callback=disconnected_callback
        )
        conn.connect()
        conn.send(MethodMessage(call_id, 'echo', ['Hello, World!']))

        with received_cond:
            while not self.received:
                received_cond.wait(timeout=1)

        conn.disconnect()

        with disconnected_cond:
            while not self.disconnected:
                disconnected_cond.wait(timeout=1)


if __name__ == '__main__':
    unittest.main()

