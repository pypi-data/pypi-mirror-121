# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dripostal']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<5.0'],
 'aiohttp': ['aiohttp>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'dripostal',
    'version': '0.1.1',
    'description': 'A tiny API client for the Pelias Libpostal REST service.',
    'long_description': '<p style="text-align: center; padding-bottom: 1rem;">\n    <a href="https://dribia.github.io/dripostal">\n        <img \n            src="https://dribia.github.io/dripostal/img/logo_dribia_blau_cropped.png" \n            alt="dripostal" \n            style="display: block; margin-left: auto; margin-right: auto; width: 40%;"\n        >\n    </a>\n</p>\n\n<p style="text-align: center">\n    <a href="https://github.com/dribia/dripostal/actions?query=workflow%3ATest" target="_blank">\n        <img src="https://github.com/dribia/dripostal/workflows/Test/badge.svg" alt="Test">\n    </a>\n    <a href="https://github.com/dribia/dripostal/actions?query=workflow%3APublish" target="_blank">\n        <img src="https://github.com/dribia/dripostal/workflows/Publish/badge.svg" alt="Publish">\n    </a>\n    <a href="https://codecov.io/gh/dribia/dripostal" target="_blank">\n        <img src="https://img.shields.io/codecov/c/github/dribia/dripostal?color=%2334D058" alt="Coverage">\n    </a>\n    <a href="https://pypi.org/project/dripostal" target="_blank">\n        <img src="https://img.shields.io/pypi/v/dripostal?color=%2334D058&label=pypi%20package" alt="Package version">\n    </a>\n</p>\n\n<p style="text-align: center;">\n    <em>A tiny API client for the Pelias Libpostal REST service.</em>\n</p>\n\n---\n\n**Documentation**: <a href="https://dribia.github.io/dripostal" target="_blank">https://dribia.github.io/dripostal</a>\n\n**Source Code**: <a href="https://github.com/dribia/dripostal" target="_blank">\nhttps://github.com/dribia/dripostal</a>\n\n---\n\n[**Libpostal**](https://github.com/openvenues/libpostal) is a widely known C library for \n**parsing and normalizing street addresses** around the world. \n\nDespite having its own Python bindings, getting to install the library can be quite hard and time-consuming.\nA common workaround is then to use a dockerized service exposing Libpostal as a REST API, \ne.g. [**Pelias\' Libpostal REST service**](https://github.com/pelias/libpostal-service).\n\n**Dripostal** aims to provide a Python interface with such API, both in the synchronous and the asynchronous ways.\n\n## Key features\n\n* Query Libpostal\'s [**`parse`**](https://github.com/openvenues/libpostal#examples-of-parsing) and [**`expand`**](https://github.com/openvenues/libpostal#examples-of-normalization) methods.\n* Return results as [**Pydantic**](https://pydantic-docs.helpmanual.io/) models.\n* Provides a mirror [**async client**](https://docs.python.org/3/library/asyncio.html) enabling asynchronous queries to the Libpostal REST service.\n\n## Example\n\nIn order to successfully run the following example, a Libpostal service should be running locally:\n\n```shell\ndocker run -d -p 4400:4400 pelias/libpostal-service\n```\n\n!!!info\n    The command above will be pulling the `libpostal-service` Docker image from **Pelias** and \n    running a container that will serve the Libpostal REST service through its port 4400.\n\n    * With option `-p 4400:4400` we are mapping port \n      `4400` in the docker container to port `4400` in the docker host, i.e. your computer. \n      You could map it to another port of the host, e.g. the `8080`, changing `4400:4400` for `8080:4400`.\n    * With option `-d` we are running the docker container in _detached mode_, i.e. in the background. \n\nNow we should be able to run the following code:\n\n```python\nfrom dripostal import DriPostal\n\ndripostal = DriPostal(url="http://0.0.0.0:4400")\n\ndripostal.parse("Planta 3 mòdul 303, Carrer de la Llacuna, 162, 08018 Barcelona")\n\n"""\nAddress(\n    house=\'mòdul 303\', \n    house_number=\'162\', \n    road=\'carrer de la llacuna\', \n    level=\'planta 3\', \n    postcode=\'08018\', \n    city=\'barcelona\', \n    country=None, \n    ...\n)\n"""\n```\n',
    'author': 'Dribia Data Research',
    'author_email': 'opensource@dribia.com',
    'maintainer': 'Nabil Kakeh',
    'maintainer_email': 'nabil@dribia.com',
    'url': 'https://dribia.github.io/dripostal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
