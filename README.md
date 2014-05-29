pyddp
=====

A Python 2 distributed data protocol (DDP) client.

_Warning_: This library is still in the planning stage. If you choose to use it,
           please use a specific commit.


Installation
------------

Install via `pip`

```Shell
$ pip install pyddp
```


Get started
-----------

```Python
import ddp
client = ddp.DdpClient('127.0.0.1:3000')
client.enable()
result = client.call('echo', 'Hello, World!')
print(result.get())
client.disable()
```

