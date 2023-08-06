# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aacoding_portal_gun']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['aacoding-portal-gun = aacoding_portal_gun.main:app']}

setup_kwargs = {
    'name': 'aacoding-portal-gun',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Portal Gun\n\nThe awesome Portal Gun',
    'author': 'Robert Zhou',
    'author_email': 'alphacodinghub@outlook.com',
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
