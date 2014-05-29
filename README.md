pyddp
=====
![Build Status Images][travisci]


Distributed data protocol (DDP) for Python 2.

_Warning_: This library is still in the planning stage. If you choose to use it,
           please use a specific commit.

Read the [documentation][docs] on ReadTheDocs.org.

Features
--------

* _Async methods calles_. Call Meteor methods just like you would using Meteor
  client-side.

    ```Python
    future = client.call('method', arg1, arg2, args3)

    # Do some work then block until the result is received.
    print future.get()
    ```

* _Automatic Reconnection_: If the connection to the server goes down, the
  client automatically attempt to reconnect.

* _Ponger_: Automatically responses to ping from the server.

* _Debugging_: ``DdpClient(..., logging=True)`` will print everything sent
  and received by the client.


### Coming soon (i.e., not implemented)

* Automating resend after reconnection
* Outboxing
* Random seeds
* Sensible reconnection delay (i.e. exponential back-off)
* Subscriptions


Installation
------------

Install via `pip`

```Shell
$ pip install pyddp
```


Get started
-----------

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
[travisci]: https://travis-ci.org/foxdog-studios/pyddp.svg "Build Status Images"
[meteor]: https://www.meteor.com/
[virtualenv]: http://virtualenv.readthedocs.org/en/latest/

