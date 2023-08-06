# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyter_flex', 'jupyter_flex.tests']

package_data = \
{'': ['*'],
 'jupyter_flex': ['templates/nbconvert/flex/conf.json',
                  'templates/nbconvert/flex/conf.json',
                  'templates/nbconvert/flex/conf.json',
                  'templates/nbconvert/flex/flex.j2',
                  'templates/nbconvert/flex/flex.j2',
                  'templates/nbconvert/flex/flex.j2',
                  'templates/nbconvert/flex/index.html.j2',
                  'templates/nbconvert/flex/index.html.j2',
                  'templates/nbconvert/flex/index.html.j2',
                  'templates/nbconvert/flex/static/*',
                  'templates/voila/flex/*']}

install_requires = \
['illusionist>=0.3.0,<0.4.0',
 'ipykernel>=6.4.1,<7',
 'jinja2>=3.0.1,<4',
 'nbconvert>=6.2.0,<7',
 'voila>=0.2.0,<0.3']

entry_points = \
{'console_scripts': ['jupyter-flex = jupyter_flex.app:main'],
 'nbconvert.exporters': ['flex = jupyter_flex:FlexExporter',
                         'flex-illusionist = '
                         'jupyter_flex:FlexIllusionistExporter']}

setup_kwargs = {
    'name': 'jupyter-flex',
    'version': '0.8.0',
    'description': 'Build dashboards using Jupyter Notebooks',
    'long_description': '# jupyter-flex: Dashboards for Jupyter\n\n[![pypi](https://badge.fury.io/py/jupyter-flex.svg)](https://pypi.org/project/jupyter-flex/)\n[![build](https://github.com/danielfrg/jupyter-flex/workflows/test/badge.svg)](https://github.com/danielfrg/jupyter-flex/actions/workflows/test.yml)\n[![docs](https://github.com/danielfrg/jupyter-flex/workflows/docs/badge.svg)](https://github.com/danielfrg/jupyter-flex/actions/workflows/docs.yml)\n[![coverage](https://codecov.io/gh/danielfrg/jupyter-flex/branch/master/graph/badge.svg)](https://codecov.io/gh/danielfrg/jupyter-flex?branch=master)\n[![license](https://img.shields.io/:license-Apache%202-blue.svg)](https://github.com/danielfrg/jupyter-flex/blob/master/LICENSE.txt)\n[![binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/danielfrg/jupyter-flex/0.8.0?urlpath=voila%2Ftree%2Fexamples)\n\nBuild dashboard using Jupyter Notebooks.\n\n- Use Markdown headers and Jupyter Notebook cell tags to define the dashboard layout and its components\n- Flexible and easy way to specify row and column based layouts\n- Use [nbconvert](https://nbconvert.readthedocs.io/en/latest/) to create static reports\n- Use [Voila](https://github.com/voila-dashboards/voila) to start a live Jupyter Kernel for fully dynamic applications\n- Support for [Jupyter widgets](https://ipywidgets.readthedocs.io/en/latest/)\n\n<a href="https://mybinder.org/v2/gh/danielfrg/jupyter-flex/0.8.0?urlpath=%2Fvoila%2Frender%2Fexamples%2Fmovie-explorer.ipynb"><img src="https://jupyter-flex.danielfrg.com/assets/img/screenshots/movie-explorer.png" alt="Jupyter-flex: Movie Explorer"  width=276></a>\n<a href="https://jupyter-flex.danielfrg.com/examples/nba-scoring.html"><img src="https://jupyter-flex.danielfrg.com/assets/img/screenshots/nba-scoring.png" alt="Jupyter-flex: NBA Scoring" width=276></a>\n<a href="https://jupyter-flex.danielfrg.com/examples/altair.html"><img src="https://jupyter-flex.danielfrg.com/assets/img/screenshots/plots/altair.png" alt="Jupyter-flex: Bokeh plots"  width=276></a>\n\n## Installation\n\n```\npip install jupyter-flex\n```\n\n## Learning More\n\nLearn more in the [jupyter-flex documentation](https://jupyter-flex.danielfrg.com).\n\n## How to Contribute\n\nSee [CONTRIBUTING.md](https://github.com/danielfrg/jupyter-flex/blob/master/CONTRIBUTING.md).\n',
    'author': 'Daniel Rodriguez',
    'author_email': 'None',
    'maintainer': 'Daniel Rodriguez',
    'maintainer_email': 'None',
    'url': 'https://github.com/danielfrg/jupyter-flex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
