# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['esbuild']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'esbuild',
    'version': '0.1.2',
    'description': 'Install and invoke esbuild from Python',
    'long_description': '# Python Esbuild\n\n[WIP]\n\nA highly experimental Python wrapper for [Esbuild](https://esbuild.github.io/), an extremely fast JavaScript bundle.\n\nAllows you to build modern JavaScript from Python without installing Node and bundlers like Webpack, Vite, Parcel,\netc...\n',
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timonweb/python-esbuild',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
