# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ultimatethumb', 'ultimatethumb.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2', 'Pillow>=8.3', 'command_executor>=0.1']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata'], 'docs': ['Sphinx>=3.5']}

setup_kwargs = {
    'name': 'django-ultimatethumb',
    'version': '1.2.0',
    'description': 'Generate thumbnails of anything.',
    'long_description': "django-ultimatethumb\n=======================\n\n.. image:: https://img.shields.io/pypi/v/django-ultimatethumb.svg\n   :target: https://pypi.org/project/django-ultimatethumb/\n   :alt: Latest Version\n\n.. image:: https://codecov.io/gh/stephrdev/django-ultimatethumb/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/stephrdev/django-ultimatethumb\n   :alt: Coverage Status\n\n.. image:: https://readthedocs.org/projects/django-ultimatethumb/badge/?version=latest\n   :target: https://django-ultimatethumb.readthedocs.io/en/stable/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://travis-ci.org/stephrdev/django-ultimatethumb.svg?branch=master\n   :target: https://travis-ci.org/stephrdev/django-ultimatethumb\n\n\n`django-ultimatethumb` is another Django library for generating thumbnails but\nhas some advantages:\n\n* Thumbnails are not generated when the templatetag is called. Instead, images\n  are generated on demand when they are requested by the browser. This can\n  lead to a major speedup of your page response times.\n* Thumbnails can be generated from static files too (for example to downscale\n  retina-optimized images and therefore reducing traffic).\n* Generate multiple thumbnail sizes at once for use in `picture` html tags with\n  multiple sources (e.g. with media queries).\n\n\nRequirements\n------------\n\ndjango-ultimatethumb supports Python 3 only and requires at least Django 1.11.\n\n\nPrepare for development\n-----------------------\n\nA Python 3.6 interpreter is required in addition to pipenv.\n\n.. code-block:: shell\n\n    $ poetry install\n\n\nNow you're ready to run the tests:\n\n.. code-block:: shell\n\n    $ make tests\n\n\nResources\n---------\n\n* `Documentation <https://django-ultimatethumb.readthedocs.io/en/latest/>`_\n* `Bug Tracker <https://github.com/stephrdev/django-ultimatethumb/issues>`_\n* `Code <https://github.com/stephrdev/django-ultimatethumb/>`_\n",
    'author': 'Stephan Jaekel',
    'author_email': 'steph@rdev.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stephrdev/django-ultimatethumb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
