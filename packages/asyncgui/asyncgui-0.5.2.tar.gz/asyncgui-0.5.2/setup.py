# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncgui', 'asyncgui.testing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asyncgui',
    'version': '0.5.2',
    'description': 'Async library that works with an existing event loop',
    'long_description': "# AsyncGui\n\nAsync library that works with an existing event loop.\nThis is not for application developers, but for async-library developers.\n\n## Pin the minor version\n\nIf you use this module, it's recommended to pin the minor version, because if it changed, it means some *important* breaking changes occurred.\n\n## Test Environment\n\n- CPython 3.7\n- CPython 3.8\n- CPython 3.9\n\n## Async-libraries who use this\n\n- [asynckivy](https://github.com/gottadiveintopython/asynckivy)\n- [asynctkinter](https://github.com/gottadiveintopython/asynctkinter)\n\n## TODO\n\n- implement `trio.Semaphore` equivalent`\n",
    'author': 'Nattōsai Mitō',
    'author_email': 'flow4re2c@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gottadiveintopython/asyncgui',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
