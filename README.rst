=============
play requests
=============


.. image:: https://img.shields.io/pypi/v/play_requests.svg
        :target: https://pypi.python.org/pypi/play_requests

.. image:: https://travis-ci.org/davidemoro/play_requests.svg?branch=develop
       :target: https://travis-ci.org/davidemoro/play_requests

.. image:: https://readthedocs.org/projects/play-requests/badge/?version=latest
        :target: https://play-requests.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://codecov.io/gh/davidemoro/play_requests/branch/develop/graph/badge.svg
     :target: https://codecov.io/gh/davidemoro/play_requests


pytest-play plugin driving the famous Python requests_ library for making ``HTTP`` calls.

More info and examples on:

* pytest-play_, documentation
* cookiecutter-qa_, see ``pytest-play`` in action with a working example if you want to start hacking


Features
--------

This pytest-play_ command provider let you drive a
Python requests_ HTTP library using a YAML configuration file
containing a set of pytest-play_ commands.

you can see a pytest-play_ script powered by a command provided
by the play_requests_ plugin:

::

    - provider: play_requests
      type: GET
      assertion: "'pytest-play' in response.json()"
      url: https://www.google.it/complete/search
      parameters:
        headers:
          Host: www.google.it
          User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101
            Firefox/57.0
          Accept: "*/*"
          Accept-Language: en-US,en;q=0.5
          Referer: https://www.google.it/
          Connection: keep-alive
        params:
        - - client
          - psy-ab
        - - hl
          - it
        - - gs_rn
          - '64'
        - - gs_ri
          - psy-ab
        - - gs_mss
          - pytest-
        - - cp
          - '11'
        - - gs_id
          - '172'
        - - q
          - pytest-play
        - - xhr
          - t
        timeout: 2.5


The above example:

* performs a GET call to https://www.google.it/complete/search?client=psy-ab&hl=it&... 
  with the provided headers, a timeout (if it takes more than 2.5 seconds a timeout
  exception will be raised) and an assertion expression that verifies that the response
  meets the expected value

play_requests_ supports all the HTTP verbs supported by the requests_ library:

* OPTIONS
* HEAD
* GET
* POST
* PUT
* PATCH
* DELETE

You'll find other play_requests_ command examples in the following sections.

Authentication cookies
======================

Manages cookies and prepare them for you so you don't have to create
cookie headers by yourself using the ``auth=('username', 'password')``::

    - provider: play_requests
      type: GET
      url: http://something/authenticated
      parameters:
        auth:
          - username
          - password

Upload files
============

Post a csv file::

    - provider: play_requests
      type: POST
      url: http://something/1
      parameters:
        files:
          filecsv:
          - report.csv
          - some,data

Post a csv file with custom headers::

    - provider: play_requests
      type: POST
      url: http://something/1
      parameters:
        files:
          filecsv:
          - report.csv
          - some,data
          - application/csv
          - Expires: '0'

Post a file providing the path::

    - provider: play_requests
      type: POST
      url: http://something/1
      parameters:
        files:
          filecsv:
          - file.csv
          - path:$base_path/file.csv

assuming that you have a ``$base_path`` variable.

Save the response to a variable
===============================

You can save a response elaboration to a pytest-play_ variable
and reuse in the following commands::

    - provider: play_requests
      type: POST
      url: http://something/1
      variable: myvar
      variable_expression: response.json()
      assertion: variables['myvar']['status'] == 'ok'
      parameters:
        json:
          foo: bar
        timeout: 2.5

It the endpoint returns a non JSON response, use ``response.text`` instead.

Default payload
===============

If all your requests have a common payload it might be annoying
but thanks to play_requests_ you can avoid repetitions.

You can set variables in many ways programatically using the pytest-play_
execute command or execute commands. You can also update variables using
the play_python_ ``exec`` command::

    - provider: python
      type: store_variable
      name: bearer
      expression: "'BEARER'"
    - provider: python
      type: store_variable
      name: play_requests
      expression: "{'parameters': {'headers': {'Authorization': '$bearer'}}}"
    - provider: play_requests
      type: GET
      url: "$base_url"

and all the following HTTP calls will be performed with the authorization bearer provided in the default
payload.

Merging rules:

* if a play_requests_ command provides any other header value, the resulting HTTP call will be performed
  with merged header values (eg: ``Authorization`` + ``Host``)
* if a play_requests_ command provides a conflicting header value or any other default option,
  the ``Authorization`` header provided by the command will win and it will override just for the current
  call the default conflicting header value

Assert response status code
===========================

::

    - provider: play_requests
      type: POST
      url: http://something/1
      variable: myvar
      variable_expression: response.json()
      assertion: response.status_code == 200
      parameters:
        json:
          foo: bar

of if you want you can use the expression ``response.raise_for_status()`` instead of
checking the exact match of status code.

The ``raise_for_status`` call will raise an ``HTTPError`` if the ``HTTP`` request
returned an unsuccessful status code.


Post raw data
=============

If you want to send some POST data or send a JSON payload without automatic JSON encoding::

    - provider: play_requests
      type: POST
      url: http://something/1
      parameters:
        data: '{"foo"  : "bar"    }'

Redirections
============

By default requests_ will perform location redirection for all verbs
except HEAD:

* http://docs.python-requests.org/en/master/user/quickstart/#redirection-and-history

You can disable or enable redirects playing with the ``allow_redirects`` option::

    - provider: play_requests
      type: POST
      url: http://something/1
      variable: myvar
      variable_expression: response.json()
      assertion: response.status_code == 200
      parameters:
        allow_redirects: false
        json:
          foo: bar

Twitter
-------

``pytest-play`` tweets happens here:

* `@davidemoro`_

Credits
-------

This package was created with Cookiecutter_ and the cookiecutter-play-plugin_ (based on `audreyr/cookiecutter-pypackage`_ project template).

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`cookiecutter-play-plugin`: https://github.com/davidemoro/cookiecutter-play-plugin
.. _pytest-play: https://github.com/davidemoro/pytest-play
.. _cookiecutter-qa: https://github.com/davidemoro/cookiecutter-qa
.. _requests: http://docs.python-requests.org/en/master/user/quickstart
.. _play_requests: https://play_requests.readthedocs.io/en/latest
.. _play_python: https://play_python.readthedocs.io/en/latest
.. _`@davidemoro`: https://twitter.com/davidemoro
