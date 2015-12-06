.. contents::
   :depth: 3
..

pygrok |Build Status|
=====================

|Join the chat at https://gitter.im/garyelephant/pygrok|

A Python library to parse strings and extract information from
structured/unstructured data

What can I use Grok for?
------------------------

-  parsing and matching patterns in a string(log, message etc.)
-  relieving from complex regular expressions.
-  extracting information from structured/unstructured data

Installation
------------

.. code:: Bash

        $ pip install pygrok

or download, uncompress and install pygrok from
`here <https://github.com/garyelephant/pygrok/releases/latest>`__:

.. code:: Bash

        $ tar zxvf pygrok-xx.tar.gz
        $ cd pygrok_dir
        $ sudo python setup.py install

Getting Started
---------------

.. code:: Python

    >>> import pygrok
    >>> text = 'gary is male, 25 years old and weighs 68.5 kilograms'
    >>> pattern = '%{WORD:name} is %{WORD:gender}, %{NUMBER:age} years old and weighs %{NUMBER:weight} kilograms'
    >>> print pygrok.grok_match(text, pattern)
    {'gender': 'male', 'age': '25', 'name': 'gary', 'weight': '68.5'}

Pretty Cool ! Some of the pattern you can use are listed here:

::

    `WORD` means \b\w+\b in regular expression.
    `NUMBER` means (?:%{BASE10NUM})
    `BASE10NUM` means (?<![0-9.+-])(?>[+-]?(?:(?:[0-9]+(?:\.[0-9]+)?)|(?:\.[0-9]+)))

    other patterns such as `IP`, `HOSTNAME`, `URIPATH`, `DATE`, `TIMESTAMP_ISO8601`, `COMMONAPACHELOG`..

See All patterns `here <./pygrok/patterns>`__

More details
------------

Beause python re module does not support regular expression syntax
atomic grouping(?>),so pygrok requires
`regex <https://pypi.python.org/pypi/regex/2014.06.28>`__ to be
installed.

pygrok is inspired by `Grok <https://github.com/jordansissel/grok>`__
developed by Jordan Sissel. This is not a wrapper of Jordan Sissel's
Grok and totally implemented by me.

Grok is a simple software that allows you to easily parse strings, logs
and other files. With grok, you can turn unstructured log and event data
into structured data.Pygrok does the same thing.

I recommend you to have a look at `logstash filter
grok <https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html>`__,
it explains how Grok-like thing work.

pattern files come from `logstash filter grok's pattern
files <https://github.com/logstash-plugins/logstash-patterns-core/tree/master/patterns>`__

Contribute
----------

-  You are encouraged to
   `fork <https://github.com/garyelephant/pygrok/fork>`__, improve the
   code, then make a pull request.
-  `Issue tracker <https://github.com/garyelephant/pygrok/issues>`__

Get Help
--------

::

    mail:garygaowork@gmail.com
    twitter:@garyelephant

Contributors
------------

Thanks to `all
contributors <https://github.com/garyelephant/pygrok/graphs/contributors>`__

.. |Build Status| image:: https://travis-ci.org/garyelephant/pygrok.svg?branch=master
   :target: https://travis-ci.org/garyelephant/pygrok
.. |Join the chat at https://gitter.im/garyelephant/pygrok| image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/garyelephant/pygrok?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
