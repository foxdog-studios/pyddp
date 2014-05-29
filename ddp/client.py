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

from ddp import pubsub

from ddp.connection import (
    ObservableWebSocketClientFactory,
    ServerUrl,
)

from ddp.id_generator import build_id_generator

from ddp.message import (
    AddedBeforeMessageParser,
    AddedMessageParser,
    ChangedMessageParser,
    ConnectedMessageParser,
    ErrorMessageParser,
    FailedMessageParser,
    MovedBeforeMessageParser,
    NosubMessageParser,
    PingMessageParser,
    PongMessageParser,
    ReadyMessageParser,
    RemovedMessageParser,
    ResultMessageParser,
    UpdatedMessageParser,

    ConnectMessageSerializer,
    MethodMessageSerializer,
    PingMessageSerializer,
    PongMessageSerializer,
    SubMessageSerializer,
    UnsubMessageSerializer,
)

from ddp.pod import (
    PodMessageFilter,
    PodMessageParser,
    PodMessageSerializer,
)

__all__ = ['DdpClient']


class DdpClient(object):
    def __init__(self, url, logging=False):
        socket_factory = ObservableWebSocketClientFactory(ServerUrl(url))
        id_generator = build_id_generator()

        self._board = board = pubsub.MessageBoard()
        self._caller = pubsub.MethodCaller(board, id_generator)

        self._components = [
            self._caller,
            pubsub.Connection(board),
            pubsub.Ponger(board),
            pubsub.Reconnector(board),
            pubsub.SocketConnection(board, socket_factory),

            pubsub.MessageParser(board, AddedBeforeMessageParser()),
            pubsub.MessageParser(board, AddedMessageParser()),
            pubsub.MessageParser(board, ChangedMessageParser()),
            pubsub.MessageParser(board, ConnectedMessageParser()),
            pubsub.MessageParser(board, ErrorMessageParser()),
            pubsub.MessageParser(board, FailedMessageParser()),
            pubsub.MessageParser(board, MovedBeforeMessageParser()),
            pubsub.MessageParser(board, NosubMessageParser()),
            pubsub.MessageParser(board, PingMessageParser()),
            pubsub.MessageParser(board, PongMessageParser()),
            pubsub.MessageParser(board, ReadyMessageParser()),
            pubsub.MessageParser(board, RemovedMessageParser()),
            pubsub.MessageParser(board, ResultMessageParser()),
            pubsub.MessageParser(board, UpdatedMessageParser()),

            pubsub.MessageSerializer(board, ConnectMessageSerializer()),
            pubsub.MessageSerializer(board, MethodMessageSerializer()),
            pubsub.MessageSerializer(board, PingMessageSerializer()),
            pubsub.MessageSerializer(board, PongMessageSerializer()),
            pubsub.MessageSerializer(board, SubMessageSerializer()),
            pubsub.MessageSerializer(board, UnsubMessageSerializer()),

            pubsub.PodMessageFilter(board, PodMessageFilter()),
            pubsub.PodMessageParser(board, PodMessageParser()),
            pubsub.PodMessageSerializer(board, PodMessageSerializer()),
        ]

        if logging:
            self._components.append(pubsub.Logger(board))

    def _connect(self):
        self._board.publish(':socket:connect')

    def _disconnect(self):
        self._board.publish(':socket:disconnect')

    def _publish(self, topic, *args, **kwargs):
        self._board.publish(topic, *args, **kwargs)

    def call(self, method, *params):
        return self._caller.call(method, list(params))

    def enable(self):
        for component in self._components:
            component.enable()
        self._connect()

    def disable(self):
        self._disconnect()
        for component in self._components:
            component.disable()

