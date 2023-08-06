# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['illusionist', 'illusionist.tests']

package_data = \
{'': ['*'],
 'illusionist': ['templates/illusionist/*', 'templates/illusionist/assets/*']}

install_requires = \
['ipywidgets>=7.6.5,<8.0.0',
 'nbclient>=0.5.0',
 'nbconvert>=6.2.0,<7',
 'nbformat>=5.0.7',
 'structlog>=21.1.0,<22.0.0']

entry_points = \
{'nbconvert.exporters': ['illusionist = illusionist:IllusionistHTMLExporter',
                         'illusionist-nb = '
                         'illusionist:IllusionistNotebookExporter']}

setup_kwargs = {
    'name': 'illusionist',
    'version': '0.3.0',
    'description': 'Interactive Jupyter Widgets without a Kernel',
    'long_description': '# illusionist\n\n[![pypi](https://badge.fury.io/py/illusionist.svg)](https://pypi.org/project/illusionist/)\n[![build](https://github.com/danielfrg/illusionist/workflows/test/badge.svg)](https://github.com/danielfrg/illusionist/actions/workflows/test.yml)\n[![docs](https://github.com/danielfrg/illusionist/workflows/docs/badge.svg)](https://github.com/danielfrg/illusionist/actions/workflows/docs.yml)\n[![coverage](https://codecov.io/gh/danielfrg/illusionist/branch/master/graph/badge.svg)](https://codecov.io/gh/danielfrg/illusionist?branch=master)\n[![license](https://img.shields.io/:license-Apache%202-blue.svg)](https://github.com/danielfrg/illusionist/blob/master/LICENSE.txt)\n\nIllusionist takes a Jupyter Notebook with widgets and converts it to a\nan HTML report that maintains the interactivity of the widgets without a\nrunning Jupyter kernel.\n\nIt does this by making all computation upfront and serializing all the possible outputs.\nIt generates a self-contained asset that you can easily drop into a file server\nand have an interactive report that scales.\n\nThe main idea of Jupyter Notebooks and Jupyter widgets is to make data closer\nto the code and data scientists while maintaining interactivity, they do a great job at that.\nIllusionist maintains the same development workflow Jupyter users are used to by using\nstandard Jupyter tooling such as `ipywidgets` and `nbconvert`.\nNo need to import anything in your notebook to generate an interactive report using illusionist,\njust run one `nbconvert` command.\n\nThe generated assets are easy to deploy, scale and have a big longevity by\nremoving a lot of deployment requirements and dependencies.\n\nLearn more and see examples in [the docs](https://illusionist.danielfrg.com/).\n',
    'author': 'Daniel Rodriguez',
    'author_email': 'None',
    'maintainer': 'Daniel Rodriguez',
    'maintainer_email': 'None',
    'url': 'https://github.com/danielfrg/mkdocs-jupyter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
