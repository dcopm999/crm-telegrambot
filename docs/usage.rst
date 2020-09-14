=====
Usage
=====

To use vacancy-telegrambot in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'telegrambot.apps.TelegrambotConfig',
        ...
    )

Add vacancy-telegrambot's URL patterns:

.. code-block:: python

    from telegrambot import urls as telegrambot_urls


    urlpatterns = [
        ...
        url(r'^', include(telegrambot_urls)),
        ...
    ]
