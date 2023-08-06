# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wisteria']

package_data = \
{'': ['*']}

install_requires = \
['rich>=10.11.0,<11.0.0']

setup_kwargs = {
    'name': 'wisteria',
    'version': '0.0.2',
    'description': 'Python serializers comparisons',
    'long_description': None,
    'author': 'suizokukan',
    'author_email': 'suizokukan@orange.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
