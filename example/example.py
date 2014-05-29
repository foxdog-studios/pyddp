#!/usr/bin/env python

import ddp

client = ddp.DdpClient('127.0.0.1:3000')
client.enable()

future = client.call('upper', 'Hello, World!')
result_message = future.get()

if result_message.has_result():
    print 'Result:', result_message.result

if result_message.has_error():
    print 'Error:', result_message.error

client.disable()

