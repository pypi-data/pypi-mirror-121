# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cyberpoweredpc']
install_requires = \
['chromedriver-autoinstaller>=0.2.2,<0.3.0',
 'easygui==0.98.2',
 'fire>=0.4.0,<0.5.0',
 'selenium==3.141.0']

setup_kwargs = {
    'name': 'cyberpoweredpc',
    'version': '0.0.8',
    'description': 'A cyber-powered PC builder for cyberpowerpc.com',
    'long_description': '# Cyber-Powered PC\n#### A cyber-powered PC builder for cyberpowerpc.com\n\n## Install\n```bash\npip3 install cyberpoweredpc\n```\n\n## Run\n```bash\n# This will show the available commands\npython3 -m cyberpoweredpc\n```',
    'author': 'DareDoes',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daredoes/cyberpoweredpc',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
