# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_sass_finder']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<4.0', 'libsass>=0.21,<0.22']

setup_kwargs = {
    'name': 'django-sass-finder',
    'version': '2.0.6',
    'description': 'A Django finder that compiles Sass files',
    'long_description': None,
    'author': 'Jesus Trujillo',
    'author_email': 'trudev.professional@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Uniquode/django_sass_finder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
