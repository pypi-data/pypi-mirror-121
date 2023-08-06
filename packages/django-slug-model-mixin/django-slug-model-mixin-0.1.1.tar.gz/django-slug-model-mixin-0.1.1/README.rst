=============================
Django Slug Model Mixin
=============================

.. image:: https://badge.fury.io/py/django-slug-model-mixin.svg
    :target: https://badge.fury.io/py/django-slug-model-mixin

.. image:: https://travis-ci.org/frankhood/django-slug-model-mixin.svg?branch=master
    :target: https://travis-ci.org/frankhood/django-slug-model-mixin

.. image:: https://codecov.io/gh/frankhood/django-slug-model-mixin/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/frankhood/django-slug-model-mixin

Overview
-------------

A slug model mixin to have slugify feature on your models

Quickstart
----------

Install Django Slug Model Mixin::

    pip install django-slug-model-mixin

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'slug_model_mixin',
        ...
    )

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtest.py


Development commands
---------------------

::

    pip install -r requirements_dev.txt


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
