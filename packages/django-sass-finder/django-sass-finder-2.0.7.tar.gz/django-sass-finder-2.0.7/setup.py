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
    'version': '2.0.7',
    'description': 'A Django finder that compiles Sass files',
    'long_description': "# Django Sass Finder\nA static files finder for Django that compiles Sass files\n\n## Installation\n### WARNING: MAKE SURE YOU HAVE NO SASS PACKAGES INSTALLED (other than libsass)!\nRun `pip install django_sass_finder` to add this module to your virtualenv,\nthen add the finder to the list your static file finders as follows:\n\n```python\nSTATICFILES_FINDERS = [\n    # add the default Django finders as this setting will override the default\n    'django.contrib.staticfiles.finders.FileSystemFinder',\n    'django.contrib.staticfiles.finders.AppDirectoriesFinder',\n    # our finder\n    'django_sass_finder.finders.ScssFinder',\n]\n```\nThere is no need to add django_sass_finder into `settings.INSTALLED_APPS`.\n\nThe following additional (with examples) settings are used and required by this staticfiles finder:\n\n```python\nBASE_DIR = ...\n\nSCSS_ROOT = BASE_DIR / 'scss'   # where the .scss files are sourced\nSCSS_COMPILE = [                # a list of filename pattern to search for within SCSS_ROOT\n    'site.scss',                # default is **/*,css (all scss source files in and below SCSS_ROOT)                                                                                                                                                                                                                                                                                            \n    'admin/admin.scss',\n]\nSCSS_INCLUDE_PATHS = [          # optional: scss compiler include paths (default = empty)\n    BASE_DIR / 'node_modules'\n]\nCSS_STYLE = 'compressed'            # optional: output format 'nested', 'expanded','compact','compressed'\nCSS_MAP = True                      # optional: generate a source map\nCSS_COMPILE_DIR = BASE_DIR / 'static' / 'css'   # The target directories for the compiled .css\nSTATICFILES_ROOT = [                            # this should be at or above the CSS_COMPILE_DIR\n    BASE_DIR / 'static'                         # but targetting {app}/static should also work\n]\n```\n\n`BASE_DIR` and variants above are `pathlib.Path` objects, but path strings can also be used.\n\n\n## Usage\nThis module dynamically compiles to target .css files, and recompiles them on demand whenever\nthey are updated.\n\nThe `collectstatic` management command compiles these, and lets the `FilesystemFinder` transfer\nthem to STATIC_ROOT. The development server is perfectly able to serve these from\nSTATICFILES_ROOT without the need to `collectstatic`.\n\n## License\nThis package is licensed under the MIT license.\n",
    'author': 'Jesus Trujillo',
    'author_email': 'trudev.professional@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tru-Dev/django_sass_finder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
