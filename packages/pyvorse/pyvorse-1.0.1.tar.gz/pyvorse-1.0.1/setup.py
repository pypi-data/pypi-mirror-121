# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvorse',
 'pyvorse.core',
 'pyvorse.data',
 'pyvorse.mathematics',
 'pyvorse.pipeline',
 'pyvorse.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyvorse',
    'version': '1.0.1',
    'description': 'Simple essentials extension library of additions to vanilla python.',
    'long_description': None,
    'author': 'Vladislav-Martian',
    'author_email': 'me.as.martian@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
