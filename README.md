pyddp
=====
![Build Status Images][Build Status Images]


A Python 2 distributed data protocol (DDP) client.

_Warning_: This library is still in the planning stage. If you choose to use it,
           please use a specific commit.

Read the [documentation](http://pyddp.readthedocs.org/en/latest/) on
ReadTheDocs.org.


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


[Build Status Images]: https://travis-ci.org/foxdog-studios/pyddp.svg "Build Status Images"
