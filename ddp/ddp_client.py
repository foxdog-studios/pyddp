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

from ddp.utils import ensure_asyncio
ensure_asyncio()

import asyncio

from autobahn.asyncio.websocket import WebSocketClientFactory

from ddp import pubsub
from ddp.id_generator import build_id_generator

from ddp.messages import (
    MethodMessageFactory,

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

__all__ = ['DDPClient']


class DDPClient(object):
    def __init__(self, loop, url, debug=False):
        super(DDPClient, self).__init__()
        ids = build_id_generator()
        self._board = board = pubsub.MessageBoard(loop)
        self._caller = pubsub.MethodCaller(board, MethodMessageFactory(ids))
        factory = WebSocketClientFactory(url=url, loop=loop)
        factory.protocol = pubsub.SocketPublisherFactory(board)
        subscribers = [
            self._caller,
            pubsub.DDPConnector(board),
            pubsub.Ponger(board),
            pubsub.Outbox(board),
            pubsub.SocketReconnector(board),
            pubsub.SocketConnector(board, loop, factory),

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

        if debug:
            subscribers.append(pubsub.Logger(board))

        for subscriber in subscribers:
            subscriber.subscribe()

    def open(self):
        self._board.publish(pubsub.SocketOpen)

    def call(self, future, method, *params):
        self._caller.call(future, method, list(params))

