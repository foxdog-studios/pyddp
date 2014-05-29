pyddp
=====
![Build Status Images][travisci]


Distributed data protocol (DDP) for Python 2.

_Warning_: This library is still in the planning stage. If you choose to use it,
           please use a specific commit.

Read the [documentation][docs] on ReadTheDocs.org.


Installation
------------

Install via `pip`

```Shell
$ pip install pyddp
```


Get started
-----------

1. Create and activate a Python 2.7 [virtuelenv][virtualenv].

2. Install dependencies using `pip`.

    ```Shell
    $ pip install -r requirements.txt
    ```

3. Check everything is working.

    ```Shell
    $ nosetests
    ```

3. Install [Meteor][meteor] and run the example meteor project.

    ```Shell
    $ cd example/meteor
    $ meteor
    ```

4. In another terminal, run example script (remember to activate the
   virtualenv).

    ```Python
    $ PYTHONPATH=. python example/example.py
    Result: HELLO, WORLD!
    ```


[docs]: http://pyddp.readthedocs.org/en/latest/
[travisci]: https://travis-ci.org/foxdog-studios/pyddp.svg "Build Status Images"
[meteor]: https://www.meteor.com/
[virtualenv]: http://virtualenv.readthedocs.org/en/latest/

