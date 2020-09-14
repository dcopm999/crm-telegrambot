=============================
vacancy-telegrambot
=============================

.. image:: https://badge.fury.io/py/vacancy-telegrambot.svg
    :target: https://badge.fury.io/py/vacancy-telegrambot

.. image:: https://travis-ci.org/dcopm999/vacancy-telegrambot.svg?branch=master
    :target: https://travis-ci.org/dcopm999/vacancy-telegrambot

.. image:: https://codecov.io/gh/dcopm999/vacancy-telegrambot/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dcopm999/vacancy-telegrambot

TelegramBot App

Documentation
-------------

The full documentation is at https://vacancy-telegrambot.readthedocs.io.

Quickstart
----------

Install vacancy-telegrambot::

    pip install vacancy-telegrambot

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'telegrambot',
        ...
    )

Add vacancy-telegrambot's URL patterns:

.. code-block:: python

    from telegrambot import urls as telegrambot_urls


    urlpatterns = [
        ...
        path('tg/', include(telegrambot_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
