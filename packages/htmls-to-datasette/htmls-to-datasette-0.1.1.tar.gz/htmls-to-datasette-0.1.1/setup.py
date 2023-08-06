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
    'version': '0.1.1',
    'description': 'Tool to index and serve HTML files. Powered by Datasette.',
    'long_description': "# htmls-to-datasette\n\nHtmls-to-datasette is a tool to index HTML files into a [Sqlite](https://sqlite.org) database so they can be searched and\nvisualized at a later time. This can be useful for web archival/web clipping purposes.\n\nThe database created is designed to be served on [Datasette](https://datasette.io/) and to allow to read the indexed\nfiles through it. \n\nThis tool was created to serve my own work flow that is:\n 1. Have a browser with [SingleFile](https://github.com/gildas-lormeau/SingleFile) extension installed.\n 2. When there is an interesting blog post or article save a full web page into one HTML using SingleFile.\n 3. The created `.html` file on the downloads folder is moved to a common repository (via cron job).\n 4. This common repository is synched to my main server (I use [Syncthing](https://syncthing.net/) for this).\n 5. On my personal server all the new HTML files are moved to the serving folder and this indexer is called to populate\n    the search database.\n 6. Datasette with an specific configuration will allow searching on these files and reading them online.\n\nThe indexing tool can insert the HTML contents on the database itself, to be served from there, or not. In this second\ncase the files will be served from the location they were indexed from. \n\n## Setup\n\nThis project uses *[Poetry](https://python-poetry.org/)* to make it easier to setup the appropriate dependencies to run.\n\nInstallation steps for *Poetry* can be checked on their [website](https://python-poetry.org/docs/#installation) but for\nmost of the cases this command line would work:\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\n*Note that you should exercise caution when running something directly from Internet.*  \n\n### Install dependencies:\n```bash\npoetry install\n```\n\n### Build\n\n```bash\npoetry build\n```\n\n### Install\n\nI use [pipx](https://pypa.github.io/pipx) for installing packages on isolated environments. You can install this package\nfrom the `dist/` directory in whichever way you prefer or you can \n[install pipx](https://pypa.github.io/pipx/installation/).  \n\nThe installation with pipx would be:\n```bash\npipx install dist/htmls-to-datasette-0.1.0.tar.gz\n```\n\n## Usage\n\n`htmls-to-datasette index [OPTIONS] [INPUT_DIRS]...` will create a database named `htmlstore.db' (by default).\n\n### Example\n\nGet into the server directory:\n```bash\ncd server\n```\n\nBecause this example requires Datasette to run you would have to get them using poetry:\n```bash\npoetry init\n```\n\nNow index the example file using `htmls-to-datasette`:\n```bash\nhtmls-to-datasette index input\n```\n\nAll files contained in `input` (`.html` and `.html`) will be indexed and a full text search index created. Whenever\nthere are new files to be indexed this command can be run in the same way.\n\nAnd now run the Datasette server:\n```bash\npoetry run datasette serve htmlstore.db -m metadata-files.json --plugins-dir=plugins\n```\n\nYou'll see the address to send your browser to on the screen. There is also a shortcut to make it easier to perform a\nfull text search. Should be reachable at http://127.0.0.1:8001/htmlstore/search just fill the query on the 'q' parameter\nand you will search over the indexed HTMLs. Click on the HTML file name will load its contents.\n\nFor this to work the server will require the files to be on their location (relative in this case). So if the `input`\nfolder is moved away or not accesible the files would be searchable but the contents will not be available.\n\nThere is an additional example that stores these files onto the Sqlite database itself. This has its advantages as\neverything needed for serving and searching the content will be contained in one file.\n\n```bash\n# You should be on the server directory\nrm htmlstore.db   # Remove the previous example's database\nhtmls-to-datasette index input --store-binary  # Index files and store its contents\n\n# Now run Datasette, note that now we need to use a different metadata as the contents needed to be served\n# in a different way (from the DB itself). \npoetry run datasette serve htmlstore.db -m metadata-binary.json --plugins-dir=plugins\n```\n\n### TODO\n\n- Clear content when extracting files.\n- Better documentation.\n",
    'author': 'Pablo Lopez-Jamar',
    'author_email': 'pablo.lopez.jamar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pjamar/htmls-to-datasette',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
