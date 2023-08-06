# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dagger_contrib',
 'dagger_contrib.serializer',
 'dagger_contrib.serializer.pandas']

package_data = \
{'': ['*']}

install_requires = \
['py-dagger>=0.3.0,<0.4.0']

extras_require = \
{'all': ['PyYAML>=5.4,<6.0', 'pandas>=1.3,<2.0'],
 'pandas': ['pandas>=1.3,<2.0'],
 'yaml': ['PyYAML>=5.4,<6.0']}

setup_kwargs = {
    'name': 'py-dagger-contrib',
    'version': '0.1.0',
    'description': 'Extensions for the Dagger library (py-dagger in PyPI).',
    'long_description': '# Dagger Contrib\n\nThis repository contains extensions and experiments using the [`py-dagger` library](https://github.com/larribas/dagger)\n',
    'author': 'larribas',
    'author_email': 'lorenzo.s.arribas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/larribas/dagger-contrib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
