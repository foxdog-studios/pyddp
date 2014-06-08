# pyddp

[![Latest Version][version badge]][pypi]
[![Downloads][downloads badge]][pypi]
[![Egg Status][egg badge]][pypi]
[![Wheel Status][wheel badge]][pypi]
[![Build Status][travisci badge]][travisci]
[![License][license badge]][pypi]

__Warning__

This library is still in the planning stage. If you use
it, please use a specific version, e.g.., in your ``requirements.txt`` add the line;

```
pyddp==0.3.0
```


__Connect to a Meteor DDP server__

  ```Python
  # Import the DDP package.
  import ddp

  # Create a client, passing the URL of the server.
  client = ddp.ConcurrentDDPClient('ws://127.0.0.1:3000/websocket')

  # Once started, the client will maintain a connection to the server.
  client.start()

  # ... Do something with it ...

  # Ask the client to stop and wait for it to do so.
  client.stop()
  client.join()

  ```


__Call a method__

  Assume your Meteor server has the following method.

  ```JavaScript
  Meteor.methods({
    upper: function (text) {
      check(text, String);
      return text.toUpperCase();
    }
  });
  ```

  ```Python
  # The method is executed asynchronously.
  future = client.call('upper', 'Hello, World!')

  # ... Do something else ...

  # Block until the result message is received.
  result_message = future.get()

  # Check if an error occured else print the result.
  if result_message.has_error():
    print result_message.error
  else:
    print result_message.result

  ```

__Automatic reconnection__

If the connection to the server goes down, the client automatically attempts to
reconnect.


__Ponger__

Automatically responds to pings from the server.


__Outbox__

Call a method while the client was not connected? Do not fear, for pyddp's
outbox will store the message until there is a connection.


__Debugging__

  ```Python
  ddp.ConcurrentDDPClient(url, debug=True)
  ```


__Not implemented__

*   Automatic resend after reconnection
*   DDP server
*   Random seeds
*   Sensible reconnection delay (i.e. exponential back-off)
*   Subscriptions


## Installation

Install via `pip`

```Shell
$ pip install pyddp
```


## Links

*   [Continuous integration][travisci]
*   [Documentation][docs]
*   [PyPI listing][pypi]


[docs]: http://pyddp.readthedocs.org/en/latest/ "pyddp documentation"
[downloads badge]: https://pypip.in/download/pyddp/badge.svg "Downloads"
[egg badge]: https://pypip.in/egg/pyddp/badge.svg "Egg Status"
[license badge]: https://pypip.in/license/pyddp/badge.svg "License"
[travisci]:https://travis-ci.org/foxdog-studios/pyddp "Continuous Integration"
[travisci badge]: https://travis-ci.org/foxdog-studios/pyddp.svg "Build Status"
[meteor]: https://www.meteor.com/ "Meteor"
[pypi]: https://pypi.python.org/pypi/pyddp/ "pydpp on PyPI"
[version badge]: https://pypip.in/version/pyddp/badge.svg "Latest Version"
[virtualenv]: http://virtualenv.readthedocs.org/en/latest/ "virtualenv"
[wheel badge]: https://pypip.in/wheel/pyddp/badge.svg "Wheel Status"

