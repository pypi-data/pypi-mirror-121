# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_esbuild',
 'django_esbuild.management',
 'django_esbuild.management.commands',
 'django_esbuild.migrations']

package_data = \
{'': ['*']}

install_requires = \
['esbuild>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'django-esbuild',
    'version': '0.1.0',
    'description': 'Install and invoke esbuild from Python',
    'long_description': '# Django Esbuild\n\n[WIP]\n\nA highly experimental Django wrapper for [Esbuild](https://esbuild.github.io/), an extremely fast JavaScript bundle.\n\nAllows you to build modern JavaScript from Python without installing Node and bundlers like Webpack, Vite, Parcel,\netc...\n',
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timonweb/django-esbuild',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
