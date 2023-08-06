# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sview']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.1,<3.0.0',
 'Sphinx>=4.2.0,<5.0.0',
 'inflection>=0.5.1,<0.6.0',
 'livereload>=2.6.3,<3.0.0',
 'py-buzz>=2.1.3,<3.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['sphinx-view = bin.sphinx_view:main']}

setup_kwargs = {
    'name': 'sphinx-view',
    'version': '0.3.0',
    'description': 'View your rendered Sphinx or ReStructuredText documents in a browser',
    'long_description': ".. image::  https://badge.fury.io/py/sphinx-view.svg\n   :target: https://badge.fury.io/py/sphinx-view\n   :alt:    Latest Published Version\n\n.. image::  https://travis-ci.org/dusktreader/py-buzz.svg?branch=integration\n   :target: https://travis-ci.org/dusktreader/py-buzz\n   :alt:    Build Status\n\n.. image::  https://readthedocs.org/projects/sphinx-view/badge/?version=latest\n   :target: http://sphinx-view.readthedocs.io/en/latest/?badge=latest\n   :alt:    Documentation Build Status\n\n*************\n sphinx-view\n*************\n\n---------------------------------------------------------------------\nView your rendered Sphinx or ReStrucutredText documents in a browser\n---------------------------------------------------------------------\n\nIf you've ever done much work with Sphinx (or any ReStructuredText) documents,\nyou know how important it is to regularly check how they look when rendered\ninto html. Often, you get your formatting wrong or introduce a syntax error.\nConstantly running sphinx-build by hand is really annoying.\n\nThere is a very nice tool called\n`restview <https://github.com/mgedmin/restview>`_ that can be used to view\nReStructuredText files, but it doesn't support all the sphinx keywords and\nfeatures. Furthermore, it doesn't render with a style\n\nThe sphinx-view application automatically renders the documents using the\n'alabaster' theme. It renders them using Sphinx itself. It is even capable of\nrendering an entire directory at once and producing a full html page with\nnavigation between sub-pages. This is very handy if, for instance, you are\nediting the ``docs`` folder of a python project.\n\nIn addition, sphinx-view will watch for changes to the documents, rebuild the\npages, and refresh the browser any time you save the documents you are viewing.\n\nSuper-quick Start\n-----------------\n - requirements: `python3.4` or greater\n - install through pip: `$ pip install sphinx-view`\n - view a document: `$ sphinx-view README.rst`\n\nFull Documentation\n------------------\n - `spinx-view documentation home <http://sphinx-view.readthedocs.io>`_\n - `raw reStructuredText docs\n   <https://github.com/dusktreader/sphinx-view/tree/master/docs>`_\n",
    'author': 'Tucker Beck',
    'author_email': 'tucker.beck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sphinx-view.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
