# Django stomp debug callback

[![Build Status](https://dev.azure.com/juntos-somos-mais-loyalty/python/_apis/build/status/django-stomp-debug-callback?branchName=master)](https://dev.azure.com/juntos-somos-mais-loyalty/python/_build/latest?definitionId=272&branchName=master)
[![Maintainability](https://sonarcloud.io/api/project_badges/measure?project=juntossomosmais_django-stomp-debug-callback&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=juntossomosmais_django-stomp-debug-callback)
[![Test Coverage](https://sonarcloud.io/api/project_badges/measure?project=juntossomosmais_django-stomp-debug-callback&metric=coverage)](https://sonarcloud.io/dashboard?id=juntossomosmais_django-stomp-debug-callback)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=juntossomosmais_django-stomp-debug-callback&metric=alert_status&token=edc3f4783b528b9c532e571bd14551c754b01d98)](https://sonarcloud.io/summary/new_code?id=juntossomosmais_django-stomp-debug-callback)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPI version](https://badge.fury.io/py/django-stomp-debug-callback.svg)](https://badge.fury.io/py/django-stomp-debug-callback)
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/juntossomosmais/django-stomp-debug-callback/blob/master/LICENSE)

This functionality helps you comprehend and enhance your callback code used with the [Django STOMP](https://github.com/juntossomosmais/django-stomp) library.

As this project uses a [view](./django_stomp_debug_callback/views.py) to call your callback function, it's possible to extract quite essential data that you can use to optimize your implementation.

See an example of this approach in action thanks to [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/):

![Django callback view utilization](docs/example.gif?raw=true)

####  Installation
pip install `django-stomp-debug-callback`

#### Django stomp debug callback configuration

Basically the configuration is simple, just insert the `django_stomp_debug_callback` on `INSTALLED_APPS` and 
in your application's `urls` code include the debug callback view route.
```python
from django.conf import settings
if settings.DEBUG:
    urlpatterns += [
        path("debug-callback/", include("django_stomp.debug_callback_view.urls")),
    ]
```

* Check if `django-stomp` stay into `INSTALLED_APPS` 

#### How to use ?

This route is a simple `POST` type route that expects to receive some parameters to trigger the callback function.

body parameter:
* `callback_function_path`: The path to callback function to be called
* `payload_body`: payload body to be sent to de callback function
* `payload_headers`: headers to be sent to de callback function

curl example
```curl
curl --request POST \
  --url http://0.0.0.0:8000/debug-callback/debug-function/ \
  --data '{
	"callback_function_path": "path.to.the.callback.function",
	"payload_body": {
		"fake": "body"
	},
	"payload_headers": {
		"fake": "headers"
	}
}'
```

#### How to use with django-debug-toolbar ?

Configuration for the [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) here.

* The first step is [install de django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html) in your app
```python
pip install django-debug-toolbar
```

* The second step is to configure the urls (Recommended only insert this rule id `DEBUG` is `True`)
```python
from django.conf import settings
if settings.DEBUG:
    urlpatterns += [
        path("debug-callback/", include("django_stomp.debug_callback_view.urls")), # django stomp callback view
        path("debug-toolbar/", include("debug_toolbar.urls")) # django debug toolbar
    ]
```

* The third step is to check the settings, these settings will include the middleware and debug apps to main settings

in your `.env`
```shell
##################
#### DEBUG LIB CONFIGURATION
DEBUG_APPS = "debug_toolbar"
DEBUG_MIDDLEWARE ="debug_toolbar.middleware.DebugToolbarMiddleware"
```

in your `setting`
```python
import os
DEBUG = True # only to developer mode never in production app
# DEBUG CONFIGURATION
if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": (lambda request: True)}
    INTERNAL_IPS = ["0.0.0.0"]

    DEBUG_APPS = os.getenv("DEBUG_APPS")
    if DEBUG_APPS:
        INSTALLED_APPS.append(*DEBUG_APPS.split(","))

    DEBUG_MIDDLEWARE = os.getenv("DEBUG_MIDDLEWARE")
    if DEBUG_MIDDLEWARE:
        MIDDLEWARE.append(*DEBUG_MIDDLEWARE.split(","))
```

Now you can see the debug panel in your admin url (localhost:8000/admin) and you can choose the route you want to see the requests to the bank in a given view with timing details and explain options and see the most problematic query of your stream.

#### Tests
You can run the tests with docker

```shell
docker-compose up tests
```

Or using `tox`

```shell
pipenv run tox
```

#### Lint + code formatter
The use of `.pre-commit-config.yaml` [flake8](https://github.com/pycqa/flake8), [black](https://black.readthedocs.io/en/stable/), [isort](https://pycqa.github.io/isort/) and [pylint](https://pylint.org/). 

You can run the `.pre-commit-config.yaml` with docker

```shell
docker-compose up lint-formatter
```

Or using `pre-commit`

```shell
pre-commit run --all-files
```