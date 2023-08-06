=============================
Nobinobi Kitchen
=============================

.. image:: https://badge.fury.io/py/nobinobi-kitchen.svg
    :target: https://badge.fury.io/py/nobinobi-kitchen

.. image:: https://travis-ci.com/prolibre-ch/nobinobi-kitchen.svg?branch=master
    :target: https://travis-ci.com/prolibre-ch/nobinobi-kitchen

.. image:: https://codecov.io/gh/prolibre-ch/nobinobi-kitchen/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/prolibre-ch/nobinobi-kitchen

Application Kitchen for Nobinobi

Documentation
-------------

The full documentation is at https://nobinobi-kitchen.readthedocs.io.

Quickstart
----------

Install Nobinobi Kitchen::

    pip install nobinobi-kitchen

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'phonenumber_field',
        'crispy_forms',
        'django_extensions',
        'rest_framework',
        'rest_framework.authtoken',
        'rest_framework_datatables',
        'menu',
        'bootstrap_modal_forms',
        'widget_tweaks',
        'django_select2',
        'bootstrap_datepicker_plus',
        'nobinobi_core',
        'nobinobi_staff',
        'nobinobi_child.apps.NobinobiChildConfig',
        'nobinobi_daily_follow_up.apps.NobinobiDailyFollowUpConfig',
        'nobinobi_kitchen.apps.NobinobiKitchenConfig',
        ...
    )

Add Nobinobi Kitchen's URL patterns:

.. code-block:: python

    from nobinobi_core import urls as nobinobi_core_urls
    from nobinobi_staff import urls as nobinobi_staff_urls
    from nobinobi_child import urls as nobinobi_child_urls
    from nobinobi_daily_follow_up import urls as nobinobi_daily_follow_up_urls
    from nobinobi_kitchen import urls as nobinobi_kitchen_urls


    urlpatterns = [
        ...
        path('', include(nobinobi_core_urls)),
        path('', include(nobinobi_staff_urls)),
        path('', include(nobinobi_child_urls)),
        path('', include(nobinobi_daily_follow_up_urls)),
        path('', include(nobinobi_kitchen_urls)),
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
