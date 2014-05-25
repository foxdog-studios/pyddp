from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from contextlib import contextmanager
from copy import copy
from urlparse import urlunparse
import json
import time
import threading

from ws4py.client.threadedclient import WebSocketClient

from ddp.messages import *
from ddp.utils import *


# =============================================================================
# = Message constants                                                         =
# =============================================================================

MSG_PING = 'ping'
MSG_PONG = 'pong'

# Client
MSG_CONNECT = 'connect'
MSG_METHOD  = 'method'
MSG_SUB     = 'sub'
MSG_UNSUB   = 'unsub'

# Server
MSG_ADDED        = 'added'
MSG_ADDED_BEFORE = 'addedBefore'
MSG_CHANGED      = 'changed'
MSG_CONNECTED    = 'connected'
MSG_ERROR        = 'error'
MSG_FAILED       = 'failed'
MSG_MOVED_BEFORE = 'movedBefore'
MSG_NOSUB        = 'nosub'
MSG_READY        = 'ready'
MSG_REMOVED      = 'removed'
MSG_RESULT       = 'result'
MSG_UPDATED      = 'updated'


# =============================================================================
# = Base message factories                                                    =
# =============================================================================

class AggregateFactory(object):
    def __init__(self, factory_classes, key):
        self._factories = {F.SRC_TYPE: F() for F in factory_classes}
        self._key = key

    def create(self, *args, **kwargs):
        key = self._key(*args, **kwargs)
        return self._factories[key].create(*args, **kwargs)


class AggregrateMessageFactory(object):
    def __init__(self, factory_classes):
        def key(pod):
            return pod['msg']
        self._factory = AggregateFactory(factory_classes, key)

    def create(self, pod):
        return self._factory.create(pod)


class AggregratePodMessageFactory(object):
    def __init__(self, factory_classes):
        self._factory = AggregateFactory(factory_classes, type)

    def create(self, message):
        return self._factory.create(message)


# = ping message factories ====================================================

class PingMessageFactory(object):
    SRC_TYPE = MSG_PING

    def create(self, pod):
        return PingMessage(id_=pod.get('id'))


class PodPingMessageFactory(object):
    SRC_TYPE = PingMessage

    def create(self, message):
        pod = {'msg': MSG_PING}
        if message.has_id():
            pod['id'] = message.id_
        return pod


# = pong message factories ====================================================

class PongMessageFactory(object):
    SRC_TYPE = MSG_PONG

    def create(self, pod):
        return PongMessage(id_=pod.get('id'))


class PodPongMessageFactory(object):
    SRC_TYPE = PongMessage

    def create(self, message):
        pod = {'msg': MSG_PONG}
        if message.has_id():
            pod['id'] = message.id_
        return pod


# =============================================================================
# = Client message factories                                                  =
# =============================================================================

# = connect messages factories ================================================

class ConnectMessageFactory(object):
    SRC_TYPE = MSG_CONNECT

    def create(self, pod):
        return ConnectMessage(
            pod['version'],
            session=pod.get('session'),
            support=pod.get('support'),
        )


class PodConnectMessageFactory(object):
    SRC_TYPE = ConnectMessage

    def create(self, message):
        pod = {
            'msg'    : MSG_CONNECT,
            'version': message.version,
        }
        if message.has_support():
            pod['support'] = message.support
        if message.has_session():
            pod['session'] = message.session
        return pod


# = method messages factories =================================================

class MethodMessageFactory(object):
    SRC_TYPE = MSG_METHOD

    def create(self, pod):
        return MethodMessage(
            pod['id'],
            pod['method'],
            pod['params'],
        )


class PodMethodMessageFactory(object):
    SRC_TYPE = MethodMessage

    def create(self, message):
        return {
            'msg'   : MSG_METHOD,
            'id'    : message.id_,
            'method': message.method,
            'params': message.params,
        }



# = sub message factories =====================================================

class SubMessageFactory(object):
    SRC_TYPE = MSG_SUB

    def create(self, pod):
        return SubMessage(
            pod['id'],
            pod['name'],
            params=pod.get('params'),
        )


class PodSubMessageFactory(object):
    SRC_TYPE = SubMessage

    def create(self, message):
        pod = {
            'msg' : MSG_SUB,
            'id'  : message.id_,
            'name': message.name
        }
        if message.has_params():
            pod['params'] = message.params
        return pod


# = unsub message factories ===================================================

class UnsubMessageFactory(object):
    SRC_TYPE = MSG_UNSUB

    def create(self, pod):
        return UnsubMessage(pod['id'])


class PodUnsubMessageFactory(object):
    SRC_TYPE = UnsubMessage

    def create(self, message):
        return {
            'msg': MSG_UNSUB,
            'id' : message.id_
        }


# = Aggregates factories ======================================================

class ClientMessageFactory(object):
    def __init__(self):
        factory_classes = [
            ConnectMessageFactory,
            MethodMessageFactory,
            PingMessageFactory,
            PongMessageFactory,
            SubMessageFactory,
            UnsubMessageFactory,
        ]
        self._factory = AggregrateMessageFactory(factory_classes)

    def create(self, message):
        return self._factory.create(message)


class PodClientMessageFactory(object):
    def __init__(self):
        factory_classes = [
            PodConnectMessageFactory,
            PodMethodMessageFactory,
            PodPingMessageFactory,
            PodPongMessageFactory,
            PodSubMessageFactory,
            PodUnsubMessageFactory,
        ]
        self._factory = AggregratePodMessageFactory(factory_classes)

    def create(self, message):
        return self._factory.create(message)


# =============================================================================
# = Server message factories                                                  =
# =============================================================================

# = added message factories ===================================================

class AddedMessageFactory(object):
    SRC_TYPE = MSG_ADDED

    def create(self, pod):
        return AddedMessage(
            pod['collection'],
            pod['id'],
            fields=pod.get('fields')
        )


class PodAddedMessageFactory(object):
    SRC_TYPE = AddedMessage

    def create(self, message):
        pod = {
            'msg'       : MSG_ADDED,
            'id'        : message.id_,
            'collection': message.collection,
        }
        if message.has_fields():
            pod['fields'] = message.fields
        return pod


# = addedBefore message factories =============================================

class AddedBeforeMessageFactory(object):
    SRC_TYPE = MSG_ADDED_BEFORE

    def create(self, pod):
        return AddedBeforeMessage(
            pod['collection'],
            pod['id'],
            pod['before'],
            pod.get('fields'),
        )


class PodAddedBeforeMessageFactory(object):
    SRC_TYPE = AddedBeforeMessage

    def create(self, message):
        pod = {
            'msg'       : MSG_ADDED_BEFORE,
            'collection': message.collection,
            'id'        : message.id_,
            'before'    : message.before,
        }
        if message.has_fields():
            pod['fields'] = message.fields
        return pod


# = changed message factories =================================================

class ChangedMessageFactory(object):
    SRC_TYPE = MSG_CHANGED

    def create(self, pod):
        return ChangedMessage(
            pod['collection'],
            pod['id'],
            cleared=pod.get('cleared'),
            fields=pod.get('fields'),
        )


class PodChangedMessageFactory(object):
    SRC_TYPE = ChangedMessage

    def create(self, message):
        pod = {
            'msg'       : MSG_CHANGED,
            'collection': message.collection,
            'id'        : message.id_,
        }
        if message.has_cleared():
            pod['cleared'] = message.cleared
        if message.has_fields():
            pod['fields'] = message.fields
        return pod


# = connected message factories ===============================================

class ConnectedMessageFactory(object):
    SRC_TYPE = MSG_CONNECTED

    def create(self, pod):
        return ConnectedMessage(pod['session'])


class PodConnectedMessageFactory(object):
    SRC_TYPE = ConnectedMessage

    def create(self, message):
        return {
            'msg'    : MSG_CONNECTED,
            'session': message.session,
        }


# = error message factories ===================================================

class ErrorMessageFactory(object):
    SRC_TYPE = MSG_ERROR

    def create(self, pod):
        return ErrorMessage(pod['reason'], pod['offendingMessage'])


class PodErrorMessageFactory(object):
    SRC_TYPE = ErrorMessage

    def create(self, message):
        return {
            'msg'             : MSG_ERROR,
            'reason'          : message.reason,
            'offendingMessage': message.offending_pod,
        }


# = failed message factories ==================================================

class FailedMessageFactory(object):
    SRC_TYPE = MSG_FAILED

    def create(self, pod):
        return FailedMessage(pod['version'])


class PodFailedMessageFactory(object):
    SRC_TYPE = FailedMessage

    def create(self, message):
        return {
            'msg'    : MSG_FAILED,
            'version': message.version,
        }


# = movedBefore message factories =============================================

class MovedBeforeMessageFactory(object):
    SRC_TYPE = MSG_MOVED_BEFORE

    def create(self, pod):
        return MovedBeforeMessage(
            pod['collection'],
            pod['id'],
            pod['before'],
        )


class PodMovedBeforeMessageFactory(object):
    SRC_TYPE = MovedBeforeMessage

    def create(self, message):
        return {
            'msg'       : MSG_MOVED_BEFORE,
            'collection': message.collection,
            'id'        : message.id_,
            'before'    : message.before,
        }


# = nosub message factories ===================================================

class NosubMessageFactory(object):
    SRC_TYPE = MSG_NOSUB

    def create(self, pod):
        return NosubMessage(pod['id'], pod.get('error'))


class PodNosubMessageFactory(object):
    SRC_TYPE = NosubMessage

    def create(self, message):
        pod = {
            'msg': MSG_NOSUB,
            'id' : message.id_,
        }
        if message.has_error():
            pod['error'] = message.error
        return pod


# = ready message factories ===================================================

class ReadyMessageFactory(object):
    SRC_TYPE = MSG_READY

    def create(self, pod):
        return ReadyMessage(pod['subs'])


class PodReadyMessageFactory(object):
    SRC_TYPE = ReadyMessage

    def create(self, message):
        return {'msg': MSG_READY, 'subs': message.subs}


# = remove message factories ==================================================

class RemoveMessageFactory(object):
    SRC_TYPE = MSG_REMOVED

    def create(self, pod):
        return RemovedMessage(
            pod['collection'],
            pod['id'],
        )


class PodRemovedMessageFactory(object):
    SRC_TYPE = RemovedMessage

    def create(self, message):
        return {
            'msg'       : MSG_REMOVED,
            'collection': message.collection,
            'id'        : message.id_,
        }


# = result message factories ==================================================

class ResultMessageFactory(object):
    SRC_TYPE = MSG_RESULT

    def create(self, pod):
        return ResultMessage(
            pod['id'],
            error=pod.get('error'),
            result=pod.get('result'),
        )


class PodResultMessageFactory(object):
    SRC_TYPE = ResultMessage

    def create(self, message):
        pod = {
            'msg': MSG_RESULT,
            'id' : message.id_,
        }
        if message.has_error():
            pod['error'] = message.error
        if message.has_result():
            pod['result'] = message.result
        return pod


# = updated message factories =================================================

class UpdatedMessageFactory(object):
    SRC_TYPE = MSG_UPDATED

    def create(self, pod):
        return UpdatedMessage(pod['methods'])


class PodUpdatedMessageFactory(object):
    SRC_TYPE = UpdatedMessage

    def create(self, message):
        return {
            'msg'    : MSG_UPDATED,
            'methods': message.methods,
        }


# = Aggregates factories ======================================================

class ServerMessageFactory(object):
    def __init__(self):
        factory_classes = [
            AddedBeforeMessageFactory,
            AddedMessageFactory,
            ChangedMessageFactory,
            ConnectedMessageFactory,
            ErrorMessageFactory,
            FailedMessageFactory,
            MovedBeforeMessageFactory,
            NosubMessageFactory,
            PingMessageFactory,
            PongMessageFactory,
            ReadyMessageFactory,
            RemoveMessageFactory,
            ResultMessageFactory,
            UpdatedMessageFactory,
        ]
        self._factory = AggregrateMessageFactory(factory_classes)

    def create(self, pod):
        return self._factory.create(pod)


class PodServerMessageFactroy(object):
    def __init__(self):
        factory_classes = [
            PodAddedBeforeMessageFactory,
            PodAddedMessageFactory,
            PodChangedMessageFactory,
            PodConnectedMessageFactory,
            PodErrorMessageFactory,
            PodFailedMessageFactory,
            PodMovedBeforeMessageFactory,
            PodNosubMessageFactory,
            PodPingMessageFactory,
            PodPongMessageFactory,
            PodReadyMessageFactory,
            PodRemovedMessageFactory,
            PodResultMessageFactory,
            PodUpdatedMessageFactory,
        ]
        self._factory = AggregratePodMessageFactory(factory_classes)

    def create(self, message):
        return self._factory.create(message)


# =============================================================================
# = Message filters                                                           =
# =============================================================================

class MessageFilter:
    pass


class PodClientMessageFilter(MessageFilter):
    def accept(self, pod):
        return True


class PodServerMessageFilter(MessageFilter):
    def accept(self, pod):
        return 'msg' in pod


# =============================================================================
# = Message parser/serializer                                                 =
# =============================================================================

class PodMessageParser(object):
    def parse(self, text):
        return json.loads(text)


class PodMessageSerializer(object):
    def serialize(self, pod):
        return json.dumps(pod)


# =============================================================================
# = Sockets                                                                   =
# =============================================================================

class WebSocketClientAdapter(WebSocketClient):
    def __init__(
        self,
        url,
        opened_callback=None,
        closed_callback=None,
        received_message_callback=None,
    ):
        super(WebSocketClientAdapter, self).__init__(url)
        self._closed_callback = closed_callback
        self._opened_callback = opened_callback
        self._received_message_callback = received_message_callback

    def opened(self):
        if exists(self._opened_callback):
            self._opened_callback()

    def received_message(self, message):
        if exists(self._received_message_callback):
            self._received_message_callback(message)

    def closed(self, code, reason=None):
        if exists(self._closed_callback):
            self._closed_callback(code, reason=reason)


class StrategyWebSocketClient(object):
    def __init__(self, *args, **kwargs):
        self._socket = WebSocketClientAdapter(*args, **kwargs)

    def connect(self, *args, **kwargs):
        return self._socket.connect(*args, **kwargs)

    def send(self, *args, **kwargs):
        return self._socket.send(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self._socket.close(*args, **kwargs)


class ServerUrl(object):
    def __init__(self, destination, scheme='ws', path='/websocket'):
        self._url = urlunparse((scheme, destination, path, '', '', ''))

    def __str__(self):
        return self._url


class MessageWebSocketClient(object):
    def __init__(
        self,
        url,
        opened_callback=None,
        received_message_callback=None,
        closed_callback=None,
    ):
        if exists(received_message_callback):
            self._received_message_callback = received_message_callback
            callback = self._received_message
        else:
            callback = None

        self._socket = StrategyWebSocketClient(
            str(url),
            opened_callback=opened_callback,
            received_message_callback=callback,
            closed_callback=closed_callback,
        )

        self._parser = PodMessageParser()
        self._filter = PodServerMessageFilter()
        self._msgfactory = ServerMessageFactory()
        self._podfactory = PodClientMessageFactory()
        self._serializer = PodMessageSerializer()

    def _received_message(self, ws_message):
        text = ws_message.data
        pod = self._parser.parse(text)
        if not self._filter.accept(pod):
            return
        message = self._msgfactory.create(pod)
        self._received_message_callback(message)

    def connect(self):
        self._socket.connect()

    def send(self, message):
        pod = self._podfactory.create(message)
        text = self._serializer.serialize(pod)
        self._socket.send(text)

    def close(self):
        self._socket.close()


class DdpConnection(object):
    def __init__(
            self,
            url,
            connected_callback=None,
            received_message_callback=None,
            disconnected_callback=None
        ):
        super(DdpConnection, self).__init__()

        self._is_connected = False
        self._pending = []

        self._connected_callback = connected_callback
        self._received_message_callback = received_message_callback
        self._disconnected_callback = disconnected_callback

        self._socket = MessageWebSocketClient(
            url,
            opened_callback=self._opened,
            received_message_callback=self._received_message,
            closed_callback=self._closed,
        )

    def _opened(self):
        msg = ConnectMessage('pre2')
        self._send(msg)

    def _send(self, message):
        self._socket.send(message)

    def _received_message(self, message):
        if isinstance(message, ConnectedMessage):
            self._is_connected = True
            if exists(self._connected_callback):
                self._connected_callback(message.session)
            for message in self._pending:
                self._send(message)
            self._pending = []
        elif isinstance(message, PingMessage):
            id_ = message.id_ if message.has_id() else None
            self._send(PongMessage(id_=id_))
        elif exists(self._received_message_callback):
            self._received_message_callback(message)

    def _closed(self, code, reason=None):
        self._is_connected = False
        if exists(self._disconnected_callback):
            self._disconnected_callback(code, reason)

    def connect(self):
        self._socket.connect()

    def send(self, message):
        if self._is_connected:
            self._send(message)
        else:
            self._pending.append(message)

    def disconnect(self):
        self._socket.close()


