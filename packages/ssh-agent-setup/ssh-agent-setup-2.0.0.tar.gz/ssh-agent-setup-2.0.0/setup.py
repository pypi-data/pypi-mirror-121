# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssh_agent_setup']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ssh-agent-setup',
    'version': '2.0.0',
    'description': 'set up a working ssh-agent and add keys for any subprocesses you want to run',
    'long_description': None,
    'author': 'Yoav Kleinberger',
    'author_email': 'haarcuba@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
