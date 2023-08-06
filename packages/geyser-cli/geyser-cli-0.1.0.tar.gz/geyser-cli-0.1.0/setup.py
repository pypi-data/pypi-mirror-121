# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geyser', 'geyser.dexs']

package_data = \
{'': ['*'], 'geyser': ['assets/*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'tabulate>=0.8.9,<0.9.0', 'web3>=5.21.0,<6.0.0']

entry_points = \
{'console_scripts': ['geyser = geyser:main']}

setup_kwargs = {
    'name': 'geyser-cli',
    'version': '0.1.0',
    'description': 'A command line utility for the Ampleforth Geyser v2',
    'long_description': "<h1 align=center><code>Geyser-cli</code></h1>\n\n`geyser-cli` is an unofficial command line utility for checking the universal \nvault(s) of a set of addresses participating in Ampleforth's Geyser v2.\n\n## Installation\n\n`pip install geyser-cli`\n\n## Setup\n\n### Ethereum node\n\n`geyser-cli` needs to talk to an Ethereum node. You can either use a local one\nor a hosted service.\nAnyway, set the node's URL as environment variable `$PROVIDER`.\n\nExample: `$ export PROVIDER=https://mainnet.infura.io/v3/<INFURA-PROJECT-ID>`\n\n## Commands\n\nChecking the available commands with `$ geyser --help` outputs:\n```\nUsage: geyser [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  claimed    Get the already claimed tokens from the user's vault(s)\n  locked     Get the tokens locked in the user's vault(s)\n  positions  Get the user's LP positions held in their vault(s)\n  status     Get the status of the user's vault(s)\n```\n\nThe `status` command is the combined output of all other commands.\n\nWith it, you can check the current status for each vault held by set of \naddresses.\n\nExample:\n```\n$ geyser status                            \\\ngov.merkleplant.eth                        \\\n0xa308de214e01c365834e3344c1088b0d2b97559c\n```\n\nOutput:\n```\ngov.merkleplant.eth\n\nNo vault(s) found...\n\n0xa308DE214e01c365834e3344C1088B0D2B97559c\n\nVault 0xa899bede339275dbd9f2c5a98e915be7f030f26f:\n\nLocked tokens:\n\nTicker                             Balance\n-------------------------------  ---------\nubAAMPL                            0.025\nSLP                                0\nUNI-V2                             0.00016\nBAL-REBASING-SMART-V1-AMPL-USDC   15\n\nClaimed tokens:\n\nTicker      Balance\n--------  ---------\nAMPL        7.85485\n\nIn Geyser Beehive:\n\nTicker      Balance\n--------  ---------\nAMPL      953.419\nWETH        0.29912\n\nIn Geyser Pescadero:\n\nTicker      Balance\n--------  ---------\nAMPL       16.4279\nWETH        0.00514\n\nIn Geyser Old Faithful:\n\nTicker      Balance\n--------  ---------\nAMPL        2.99358\nUSDC        5.91427\n```\n\n_Note that the output contains colors and other stylings not shown above._\n\n## Support\n\nIf there are any question, don't hesitate to ask!\n\nYou can reach me at pascal [at] merkleplant.xyz or in the official Ampleforth\nDiscord.\n\n## Contributions\n\nAny kind of contribution is highly welcome!\n\n## Acknowledgment\n\nThis project is heavily inspired by [uniswap-python](https://github.com/uniswap-python/uniswap-python).\n",
    'author': 'pascal-merkleplant',
    'author_email': 'pascal@merkleplant.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
