# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['texasholdem',
 'texasholdem.card',
 'texasholdem.evaluator',
 'texasholdem.game',
 'texasholdem.gui']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'texasholdem',
    'version': '0.1.0',
    'description': 'A texasholdem python package',
    'long_description': None,
    'author': 'Evyn Machi',
    'author_email': 'evyn.machi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
