

.. image:: https://github.com/snake-soft/django-git-changelog/actions/workflows/django.yml/badge.svg
   :target: https://github.com/snake-soft/django-git-changelog/actions/workflows/django.yml
   :alt: Tests

.. image:: https://api.codeclimate.com/v1/badges/34cf134656b57fd5ed21/maintainability
   :target: https://codeclimate.com/github/snake-soft/django-git-changelog/maintainability
   :alt: Maintainability


.. image:: https://codecov.io/gh/snake-soft/django-git-changelog/branch/main/graph/badge.svg?token=AP4CQNNOKZ
   :target: https://codecov.io/gh/snake-soft/django-git-changelog
    

====================
Changelog for Django
====================

This needs some work to be used in productive.


Installation
------------

Install using pip:

.. code-block:: bash

	pip install django-changelog


.. code-block:: python

   # settings.py
   INSTALLED_APPS = [
       # ...
       'changelog.apps.ChangelogConfig',
       # ...
   ]
