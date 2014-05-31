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
pyddp==0.2.2
```


__Connect to a DDP server__ (e.g., a Meteor server)

  ```Python
  # Import the DDP package.
  import ddp
  
  # Create a client, passing the host and port of the server.
  client = ddp.DdpClient('127.0.0.1:3000')
  
  # Once enabled, the client will maintain a connection to the server.
  client.enable()
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
  future = client.call('upper', 'Hello, World1')
  
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

If the connection to the server goes down, the client automatically attempts to reconnect.


__Ponger__

Automatically responds to pings from the server.


__Debugging__

  ```Python
  client = ddp.DdpClient('127.0.0.1:3000', logging=True)
  ```


__Coming soon__ (i.e., not implemented)

*   Automatic resend after reconnection
*   DDP server
*   Outboxing
*   Random seeds
*   Sensible reconnection delay (i.e. exponential back-off)
*   Subscriptions


## Installation

Install via `pip`

```Shell
$ pip install pyddp
```


## Get started

1. Create and activate a Python 2.7 [virtualenv][virtualenv].

    ```Shell
    $ virtualenv -p python2.7 venv
    $ . venv/bin/activate
    ```

2. Install dependencies using `pip`.

    ```Shell
    $ pip install -r requirements.txt
    ```

3. Check that everything is works.

    ```Shell
    $ nosetests
    ```

3. Install [Meteor][meteor] and run the example Meteor project.

    ```Shell
    $ cd example/meteor
    $ meteor
    ```

4. In another terminal, activate the virtualenv (see step 1) and run the example
   script.

    ```Shell
    $ PYTHONPATH=. python example/example.py
    Result: HELLO, WORLD!
    ```


## Links

*   [Continuous integration][travisci]
*   [Documentation][docs]
*   [PyPI listing][pypi]


[docs]: http://pyddp.readthedocs.org/en/latest/ "pyddp documentation"
[downloads badge]: https://pypip.in/download/pyddp/badge.svg "Downloads"
[egg badge]: https://pypip.in/egg/pyddp/badge.svg "Egg Status"
[license badge]: https://pypip.in/license/pyddp/badge.svg "License"
[travisci]:https://travis-ci.org/foxdog-studios/pyddp "Build Status"
[travisci badge]: https://travis-ci.org/foxdog-studios/pyddp.svg "Build Status"
[meteor]: https://www.meteor.com/ "Meteor"
[pypi]: https://pypi.python.org/pypi/pyddp/ "pydpp on PyPI"
[version badge]: https://pypip.in/version/pyddp/badge.svg "Latest Version"
[virtualenv]: http://virtualenv.readthedocs.org/en/latest/ "virtualenv"
[wheel badge]: https://pypip.in/wheel/pyddp/badge.svg "Wheel Status"

