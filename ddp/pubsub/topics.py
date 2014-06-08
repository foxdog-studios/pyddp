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

from ddp.messages.constants import MSG_PING, MSG_PONG
from ddp.messages.client.constants import MSG_CONNECT, MSG_METHOD
from ddp.messages.server.constants import MSG_CONNECTED, MSG_RESULT
from .topic import Topic

__all__ = [
    'Message',
    'MessageReceived',
    'MessageReceivedConnected',
    'MessageReceivedMethod',
    'MessageReceivedPing',
    'MessageReceivedResult',
    'MessageSend',
    'MessageSendConnect',
    'MessageSendMethod',
    'MessageSendPong',
    'Pod',
    'PodAccepted',
    'PodReceived',
    'PodRejected',
    'PodSend',
    'Raw',
    'RawReceived',
    'RawSend',
    'Socket',
    'SocketClose',
    'SocketClosed',
    'SocketError',
    'SocketOpen',
    'SocketOpened',
]

DDP = Topic('ddp')
DDPConnected = DDP + 'connected'

Message = Topic('message')

MessageReceived = Message + 'received'
MessageReceivedConnected = MessageReceived + MSG_CONNECTED
MessageReceivedMethod = MessageReceived + MSG_METHOD
MessageReceivedPing = MessageReceived + MSG_PING
MessageReceivedResult = MessageReceived + MSG_RESULT

MessageSend = Message + 'send'
MessageSendConnect = MessageSend + MSG_CONNECT
MessageSendMethod = MessageSend + MSG_METHOD
MessageSendPong = MessageSend + MSG_PONG

Pod = Topic('pod')
PodAccepted = Pod + 'accepted'
PodReceived = Pod + 'received'
PodRejected = Pod + 'rejected'
PodSend = Pod + 'send'

Raw = Topic('raw')
RawReceived = Raw + 'received'
RawSend = Raw + 'send'

Socket = Topic('socket')
SocketClose = Socket + 'close'
SocketClosed = Socket + 'closed'
SocketError = Socket + 'error'
SocketOpen = Socket + 'open'
SocketOpened = Socket + 'opened'

