# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['request_position']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.0,<4.0.0', 'geoip2>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'django-request-position',
    'version': '1.0.0',
    'description': "Django app to add a 'position' field to the request, using GeoIP or GPS data given in the request headers.",
    'long_description': 'Django Request Position\n=======================\n\nDjango app to add a "position" field to the request, using GeoIP or GPS data given in the request headers. Some\nreferences about this:\n\n* `A Uniform Resource Identifier for Geographic Locations (\'geo\' URI) <http://tools.ietf.org/rfc/rfc5870>`_.\n* `HTTP Geolocation draft-thomson-geopriv-http-geolocation-00 <http://tools.ietf.org/html/draft-thomson-geopriv-http-geolocation-00>`_.\n\n\nQuick start\n-----------\n\n**1** Install using pip::\n\n    pip install django-request-position\n\n**2** Add "request_position" to your INSTALLED_APPS settings like this::\n\n    INSTALLED_APPS += (\'request_position\',)\n\n\n**3** Add the middleware::\n\n    MIDDLEWARE += (\n        \'request_position.middleware.RequestPositionMiddleware\',\n    )\n\n\nSettings\n--------\n\n* ``REQUEST_POSITION_REMOTE_ADDR_ATTR`` (default: "REMOTE_ADDR")\n* ``REQUEST_POSITION_DEFAULT_IP`` (default: "127.0.0.1")\n* ``REQUEST_POSITION_DEFAULT_POSITION`` (default: None)\n* ``REQUEST_POSITION_DEFAULT_COUNTRY_CODE`` (default: None)\n* ``REQUEST_POSITION_COOKIE_NAME`` (default: "_request_position")\n* ``REQUEST_POSITION_GEO_HEADER`` (default: "HTTP_GEOLOCATION")\n* ``REQUEST_POSITION_OVERRIDE_LATITUDE_PARAM`` (default "lat")\n* ``REQUEST_POSITION_OVERRIDE_LONGITUDE_PARAM`` (default "lon")\n* ``REQUEST_POSITION_OVERRIDE_COUNTRY_CODE_PARAM`` (default "cc")\n* ``REQUEST_POSITION_USE_GIS_POINT`` (default False)\n',
    'author': 'Marcos Gabarda',
    'author_email': 'hey@marcosgabarda.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marcosgabarda/django-request-position',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
