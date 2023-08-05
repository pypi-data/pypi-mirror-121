# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netrunner',
 'netrunner.connections',
 'netrunner.host',
 'netrunner.runner',
 'netrunner.task']

package_data = \
{'': ['*']}

install_requires = \
['asyncssh>=2.7.0,<3.0.0',
 'genie>=21.8,<22.0',
 'pyats>=21.8,<22.0',
 'scrapli>=2021.1.30,<2022.0.0']

setup_kwargs = {
    'name': 'netrunner',
    'version': '0.1.6',
    'description': 'Network asyncio command runner using Scrapli',
    'long_description': '[![Supported Versions](https://img.shields.io/pypi/pyversions/netrunner)](https://pypi.org/project/netrunner)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nNetrunner\n===\n\nAn async network command runner built using Scrapli.\nYou provide and inventory and tasks (functions), and the runner does the rest.\n\nCurrently only working with Cisco IOS and NXOS devices, but I will be adding others.\n\n## Installation\n---\n```\npip install netrunner\n```\n\n## Basic Usage\n---\nHere is a basic example. More examples can be found in the examples folder.\n```python\nimport asyncio\n\nfrom netrunner import Runner\n\nhosts = [\n    {"hostname": "SW1021", "ip": "10.0.0.9", "platform": "ios"},\n    {"hostname": "SW1031", "ip": "10.0.0.10", "platform": "ios"},\n    {"hostname": "NX1001", "ip": "10.0.0.11", "platform": "nxos"},\n    {"hostname": "NX2001", "ip": "10.0.0.12", "platform": "nxos"},\n]\n\n\n# Here is a task. The first parameter is the host and must be provided.\n# Other parameters can also be passed into the tasks/functions.\n# Please see the examples in the example folder.\nasync def first_task(host):\n    # Commands must be passed in via a list. By default the output is parsed using\n    # Genie, but parse can be set to False if raw output is required\n    result = await host.send_command(["show version", "show vlan"])\n    return result\n\n\nasync def main():\n    # Hosts can either be passed here to be used globally, or can be passed per task\n    runner = Runner(username="test_user", password="T3stpass", hosts=hosts)\n    result = await runner.run(name="Check Version and Vlan", task=first_task)\n    print(result.run_time)\n    print(result.result["show version"])\n    print(result.result["show vlan"])\n    print(result.failed)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\n',
    'author': 'Ryan Bradshaw',
    'author_email': 'ryan@rbradshaw.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rbraddev/netrunner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
