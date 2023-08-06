# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autosave']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0']

setup_kwargs = {
    'name': 'autosave',
    'version': '1.0.0.post1',
    'description': 'Autosaving dictionary-like file objects',
    'long_description': "# autosave\n\n## Installation\n\n```sh\npip install autosave\n```\n\n## Example\n\n```py\nfrom autosave import File, AppStorage\n\n\n\n# When editing multiple entries,\n# use a with statement to only save on exit.\n\nwith File('my_file.json') as data:\n    data['dessert'] = 'pancakes'\n    data['genre'] = 'jazz'\n\n\n# By indexing entries on their own, the file is saved on each edit.\n# This is adviced against if you're editing multiple entries at a time,\n# as it is much less performant.\n\nfile = File('my_file.json')\n\nfile['garbage'] = 'smooth' + file['genre']\n\n\n# Get access to the right directories for your app,\n# by using this wrapper around `appdirs`\n\napp = AppStorage('MyApp')\napp.data / 'plugins/baguette.json'\n```",
    'author': 'Maximillian Strand',
    'author_email': 'maximillian.strand@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/deepadmax/autosave',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
