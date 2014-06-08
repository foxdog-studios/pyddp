#!/usr/bin/env python

import logging
logging.basicConfig()

import ddp

client = ddp.ConcurrentDDPClient('ws://127.0.0.1:3000/websocket', debug=False)
client.start()

future = client.call('upper', 'Hello, World!')
result_message = future.get()

if result_message.has_result():
    print 'Result:', result_message.result
if result_message.has_error():
    print 'Error:', result_message.error

client.stop()
client.join()

