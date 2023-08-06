# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kaskade', 'kaskade.widgets']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.1,<9.0.0',
 'confluent-kafka>=1.7.0,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'rich>=10.9.0,<11.0.0',
 'textual>=0.1.12,<0.2.0']

entry_points = \
{'console_scripts': ['kaskade = kaskade.app:main']}

setup_kwargs = {
    'name': 'kaskade',
    'version': '0.1.0',
    'description': 'kaskade is a terminal user interface for kafka',
    'long_description': '<pre style="font-family:Menlo,\'DejaVu Sans Mono\',consolas,\'Courier New\',monospace">\n<span style="color: #800080; text-decoration-color: #800080">╔══════════════════════════════════════╗</span>\n<span style="color: #800080; text-decoration-color: #800080">║</span> <span style="color: #800080; text-decoration-color: #800080"> _             _             _      </span> <span style="color: #800080; text-decoration-color: #800080">║</span>\n<span style="color: #800080; text-decoration-color: #800080">║</span> <span style="color: #800080; text-decoration-color: #800080">| | ____ _ ___| | ____ _  __| | ___ </span> <span style="color: #800080; text-decoration-color: #800080">║</span>\n<span style="color: #800080; text-decoration-color: #800080">║</span> <span style="color: #800080; text-decoration-color: #800080">| |/ / _` / __| |/ / _` |/ _` |/ _ \\</span> <span style="color: #800080; text-decoration-color: #800080">║</span>\n<span style="color: #800080; text-decoration-color: #800080">║</span> <span style="color: #800080; text-decoration-color: #800080">|   &lt; (_| \\__ \\   &lt; (_| | (_| |  __/</span> <span style="color: #800080; text-decoration-color: #800080">║</span>\n<span style="color: #800080; text-decoration-color: #800080">║</span> <span style="color: #800080; text-decoration-color: #800080">|_|\\_\\__,_|___/_|\\_\\__,_|\\__,_|\\___|</span> <span style="color: #800080; text-decoration-color: #800080">║</span>\n<span style="color: #800080; text-decoration-color: #800080">╚══════════════════════════════════════╝</span>\n</pre>\n\n<a href="https://github.com"><img alt="GitHub" src="https://img.shields.io/badge/-github-orange?logo=github&logoColor=white"></a>\n<a href="https://github.com/sauljabin/kaskade"><img alt="GitHub" src="https://img.shields.io/badge/status-active-success"></a>\n<a href="https://github.com/sauljabin/kaskade"><img alt="GitHub" src="https://badges.pufler.dev/updated/sauljabin/kaskade?label=updated"></a>\n<a href="https://github.com/sauljabin/kaskade/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/github/license/sauljabin/kaskade"></a>\n<a href="https://github.com/sauljabin/kaskade/actions"><img alt="GitHub Actions" src="https://img.shields.io/github/checks-status/sauljabin/kaskade/main?label=tests"></a>\n<a href="https://app.codecov.io/gh/sauljabin/kaskade"><img alt="Codecov" src="https://img.shields.io/codecov/c/github/sauljabin/kaskade"></a>\n<br>\n<a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/-python-success?logo=python&logoColor=white"></a>\n<a href="https://pypi.org/project/kaskade"><img alt="Version" src="https://img.shields.io/pypi/v/kaskade?label=kaskade"></a>\n<a href="https://pypi.org/project/kaskade"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/kaskade"></a>\n<a href="https://libraries.io/pypi/kaskade"><img alt="Dependencies" src="https://img.shields.io/librariesio/release/pypi/kaskade"></a>\n<a href="https://pypi.org/project/kaskade"><img alt="Platform" src="https://img.shields.io/badge/platform-linux%20%7C%20osx-0da5e0"></a>\n<br>\n<a href="https://www.docker.com/"><img alt="Docker" src="https://img.shields.io/badge/-docker-blue?logo=docker&logoColor=white"></a>\n<a href="https://hub.docker.com/r/sauljabin/kaskade"><img alt="Docker Image Version (latest by date)" src="https://img.shields.io/docker/v/sauljabin/kaskade?label=tag"></a>\n<a href="https://hub.docker.com/r/sauljabin/kaskade"><img alt="Docker Image Size (latest by date)" src="https://img.shields.io/docker/image-size/sauljabin/kaskade"></a>\n<br>\n<a href="https://kafka.apache.org/"><img alt="Kafka" src="https://img.shields.io/badge/-kafka-grey?logo=apache-kafka&logoColor=white"></a>\n<a href="https://kafka.apache.org/"><img alt="Kafka" src="https://img.shields.io/badge/kafka-2.8%20%7C%203.0-blue"/></a>\n<a href="https://pypi.org/project/confluent-kafka/"><img alt="Kafka Client" src="https://img.shields.io/pypi/v/confluent-kafka?label=kafka%20client"></a>\n\n`kaskade` is a terminal user interface for [kafka](https://kafka.apache.org/).\n\n# Installation and Usage\n\nInstall with pip:\n```sh\npip install kaskade\n```\n\nUpgrade with pip:\n```sh\npip install --upgrade kaskade\n```\n\nHelp:\n```sh\nkaskade --help\n```\n\nVersion:\n```sh\nkaskade --version\n```\n\nRun without config file (it\'ll take any of `kaskade.yml`, `kaskade.yaml`, `config.yml`, `config.yaml`):\n```sh\nkaskade\n```\n\nRun with config file:\n```sh\nkaskade my-file.yml\n```\n\n# Running with Docker\n\nUsing docker (add a `network` and `volume`):\n```sh\ndocker run --rm -it --network kafka-sandbox_network -v $(pwd)/config.yml:/kaskade/config.yml sauljabin/kaskade:latest\n```\n\n# Development\n\nInstalling poetry:\n```sh\npip install poetry\n```\n\nInstalling development dependencies:\n```sh\npoetry install\n```\n\nBuild (it\'ll create the `dist` folder):\n```sh\npoetry build\n```\n\n### Scripts\n\nRunning unit tests:\n```sh\npoetry run python -m scripts.tests\n```\n\nRunning multi version tests (`3.7`, `3.8`, `3.9`):\n\n> Make sure you have `python3.7`, `python3.8`, `python3.9` aliases installed\n\n```sh\npoetry run python -m scripts.multi-version-tests\n```\n\nApplying code styles:\n```sh\npoetry run python -m scripts.styles\n```\n\nRunning code analysis:\n```sh\npoetry run python -m scripts.analyze\n```\n\nRunning code coverage:\n```sh\npoetry run python -m scripts.tests-coverage\n```\n\nGenerate readme banner:\n```sh\npoetry run python -m scripts.banner\n```\n\nRunning cli using `poetry`:\n```sh\npoetry run kaskade\n```\n\n### Docker\n\nBuild docker:\n```sh\npoetry build\ndocker build -t sauljabin/kaskade:latest -f ./docker/Dockerfile .\n```\n\nRun with docker:\n```sh\ndocker run --rm -it --network kafka-sandbox_network -v $(pwd)/config.yml:/kaskade/config.yml sauljabin/kaskade:latest\n```',
    'author': 'Saúl Piña',
    'author_email': 'sauljabin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sauljabin/kaskade',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
