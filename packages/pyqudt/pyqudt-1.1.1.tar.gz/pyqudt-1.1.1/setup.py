# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qudt', 'qudt.ontology', 'qudt.ontology.resources', 'qudt.units', 'qudt.uo']

package_data = \
{'': ['*']}

install_requires = \
['PyLD>=2.0.3,<3.0.0', 'rdflib>=6.0.1,<7.0.0']

setup_kwargs = {
    'name': 'pyqudt',
    'version': '1.1.1',
    'description': 'Python library for working with the QUDT (Quantity, Unit, Dimension and Type) ontology.',
    'long_description': None,
    'author': 'Garrett Brown',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
