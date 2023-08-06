# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wisteria']

package_data = \
{'': ['*']}

install_requires = \
['rich>=10.11.0,<11.0.0']

entry_points = \
{'console_scripts': ['wisteria = wisteria.wisteria:main']}

setup_kwargs = {
    'name': 'wisteria',
    'version': '0.0.5',
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
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
