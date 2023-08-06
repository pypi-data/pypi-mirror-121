# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyqadmin']
setup_kwargs = {
    'name': 'pyqadmin',
    'version': '1.0.0',
    'description': 'pyqadmin',
    'long_description': None,
    'author': 'queryz',
    'author_email': 'queryzram@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
