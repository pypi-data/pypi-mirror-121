# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lit_data']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0']

setup_kwargs = {
    'name': 'lit-data',
    'version': '0.1.0',
    'description': 'Library to access Lithuanian open data from various official sources',
    'long_description': '# LitData 🇱🇹\n\nPython library to access Lithuanian open data from various official sources.\n',
    'author': 'Kornelijus Tvarijanavičius',
    'author_email': 'kornelijus@tvaria.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kornelijus/lit-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
