# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tortfunc', 'tortfunc.timeout']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.11.1,<2.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['importlib-metadata>=4.8.1,<5.0.0',
                                                         'typing-extensions>=3.10.0,<4.0.0']}

setup_kwargs = {
    'name': 'tortfunc',
    'version': '1.1.0',
    'description': 'Library for running Python functions with timeout and retry support.',
    'long_description': 'TimeOut and ReTry (tort)\n========================\n\nLibrary for running Python functions with timeout and retry support.\n\n\nImplementations\n===============\n\nThread\n------\n\nThe thread based implementation is based on the Killable thread concept from Tomer Filiba: http://tomerfiliba.com/recipes/Thread2/\n',
    'author': 'KLMatlock',
    'author_email': 'kevin.matlock@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
