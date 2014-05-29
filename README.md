# pyddp

[![Latest Version][version badge]][pypi]
[![Downloads][downloads badge]][pypi]
[![Egg Status][egg badge]][pypi]
[![Wheel Status][wheel badge]][pypi]
[![Build Status][travisci badge]][travisci]
[![License][license badge]][pypi]

Distributed data protocol (DDP) for Python 2.

_Warning_: This library is still in the planning stage. If you choose to use it,
           please use a specific commit.

Read the [documentation][docs] on ReadTheDocs.org.

## Features

* __Async methods calls__. Call Meteor methods just like you would using Meteor
  client-side.

    ```Python
    future = client.call('method', arg1, arg2, args3)

    # Do some work then block until the result is received.
    print future.get()
    ```

* __Automatic Reconnection__: If the connection to the server goes down, the
  client automatically attempt to reconnect.

* __Ponger__: Automatically responses to ping from the server.

* __Debugging__: ``DdpClient(..., logging=True)`` will print everything sent
  and received by the client.


### Coming soon (i.e., not implemented)

* Automating resend after reconnection
* Outboxing
* Random seeds
* Sensible reconnection delay (i.e. exponential back-off)
* Subscriptions


## Installation

Install via `pip`

```Shell
$ pip install pyddp
```


## Get started

1. Create and activate a Python 2.7 [virtuelenv][virtualenv].

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


[docs]: http://pyddp.readthedocs.org/en/latest/
[downloads badge]: https://pypip.in/download/pyddp/badge.svg
[egg badge]: https://pypip.in/egg/pyddp/badge.svg "Egg Status"
[license badge]: https://pypip.in/license/pyddp/badge.svg "License"
[travisci]:https://travis-ci.org/foxdog-studios/pyddp "Build Status"
[travisci badge]: https://travis-ci.org/foxdog-studios/pyddp.svg "Build Status"
[meteor]: https://www.meteor.com/
[pypi]: https://pypi.python.org/pypi/pyddp/
[version badge]: https://pypip.in/version/pyddp/badge.svg "Latest Version"
[virtualenv]: http://virtualenv.readthedocs.org/en/latest/
[wheel badge]: https://pypip.in/wheel/pyddp/badge.svg "Wheel Status"
