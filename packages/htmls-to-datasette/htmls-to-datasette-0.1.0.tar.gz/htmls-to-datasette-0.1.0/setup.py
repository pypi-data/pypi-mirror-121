# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htmls_to_datasette']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'datasette-render-html>=0.1.2,<0.2.0',
 'html2text>=2020.1.16,<2021.0.0',
 'rich>=10.10.0,<11.0.0',
 'sqlite-utils>=3.17,<4.0']

entry_points = \
{'console_scripts': ['htmls-to-datasette = htmls_to_datasette.cli:cli']}

setup_kwargs = {
    'name': 'htmls-to-datasette',
    'version': '0.1.0',
    'description': 'Tool to index and serve HTML files. Powered by Datasette.',
    'long_description': None,
    'author': 'Pablo Lopez-Jamar',
    'author_email': 'pablo.lopez.jamar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
