# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sheet2linkml',
 'sheet2linkml.source',
 'sheet2linkml.source.gsheetmodel',
 'sheet2linkml.terminologies',
 'sheet2linkml.terminologies.tccm']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'linkml-runtime>=1.1.2,<2.0.0',
 'pygsheets>=2.0.4,<3.0.0',
 'requests>=2.26,<3.0',
 'setuptools>=52.0.0,<53.0.0']

entry_points = \
{'console_scripts': ['sheet2linkml = sheet2linkml.cli:main']}

setup_kwargs = {
    'name': 'sheet2linkml',
    'version': '1.0.0',
    'description': 'Google Sheets to LinkML generator for the CRDC-H model',
    'long_description': '# sheet2linkml\nA python package for converting the CRDC-H data model, which is currently stored in a \n[Google Sheet](https://docs.google.com/spreadsheets/d/1oWS7cao-fgz2MKWtyr8h2dEL9unX__0bJrWKv6mQmM4/). The command line utility built into the package can be used \nto generate a [LinkML](https://github.com/linkml/linkml) representation of the CRDC-H data model.\n',
    'author': 'Gaurav Vaidya',
    'author_email': 'gaurav@renci.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cancerDHC/sheet2linkml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
