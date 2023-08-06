# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cyberpoweredpc']
install_requires = \
['chromedriver-autoinstaller>=0.2.2,<0.3.0',
 'fire>=0.4.0,<0.5.0',
 'requests>=2.26.0,<3.0.0',
 'selenium==3.141.0']

setup_kwargs = {
    'name': 'cyberpoweredpc',
    'version': '0.0.3',
    'description': 'A cyber-powered PC builder for cyberpowerpc.com',
    'long_description': None,
    'author': 'DareDoes',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
