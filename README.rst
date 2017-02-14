Spotify search demo
===============================

How to use
==========
Install requirements::

    $ pip install -r requirements.txt

Run HTTP server::

    $ make runserver

Open the website in a browser::

    http://127.0.0.1:8080/


Requirements
============
Python 3.5+, aiohttp and aiohttp-jinja2 for templating support
(see ``requirements.txt`` for more details)


Main components
===============
* HTTP server
* Spotify API wrapper, reusable for both traditional web and JSON API usage


Configuring
===========
Most of the values worth to configure are extracted into ``settings.py``. Feel
free to set them up according to your project environment. Currently they are
just host and port for the HTTP server.


Notes
=====
Take a look onto the optional JSON API endpoint at::

    http://127.0.0.1:8080/search

It can be used as a base for building single-page applications.


TODO
====
* tests
* HTML and CSS cleanup
