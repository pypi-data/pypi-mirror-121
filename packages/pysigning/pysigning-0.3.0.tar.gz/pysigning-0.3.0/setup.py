# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysigning']

package_data = \
{'': ['*']}

install_requires = \
['argh>=0.26.2,<0.27.0', 'pycryptodome>=3.10.1,<4.0.0']

entry_points = \
{'console_scripts': ['pysigning = pysigning.__main__:cli']}

setup_kwargs = {
    'name': 'pysigning',
    'version': '0.3.0',
    'description': 'Python library and CLI scripts for signing and verifying data',
    'long_description': '# pysigning\n\n> Python library and CLI scripts for signing and verifying data\n\n\n## Install\n\n```\npip3 install -U pysigning\n```\n\n## Usage\n\n### CLI\n\nGenerate a signature for the file `LICENSE` using the private key `sign.key`\n```\n$ pysigning sign @LICENSE --key sign.key\ngdFNOO9cwpYXWv9TfulFauNQ5S1WXXIQAuXC4qQB9vyOMhZW0hOl0fvyyHC1pNzZAOrpUNEoQuvvs6w2r0TdzcMsA_finu5RVVzzko4kQuOWM6Tw3CX6ln82h8z2gWyKRhIC71pScpy7MJO8IEFBBPqQbR5NDFvGVh9F69S3pVZzf4xqrkcBBWoJr2DjD-VFQ6S5hFA0PQ685cDY26hB07MWoLVHFz5jyqDfDmGqNRb5bY7fUzmJCdY5wdLExrrJQJaZhU9Ak_HAA3zsmvy0OSRTNJY7BIwVdopQ_dN-CdTLQgsoEfqpvLVp6HLRuZWhftnMlkmq0vTypgh24kYyCg==\n```\n\nVerify the signature of the file `LICENSE` using the public key `sign.crt`\n```\n$ pysigning sign @LICENSE --key sign.key | pysigning verify @LICENSE - --key sign.crt\nTrue\n```\n\n### Library\n\n```py\nimport pysigning\n\n# Generate a signature for the file `LICENSE` using the private key `sign.key`\nsig = pysigning.sign(\'@LICENSE\', key="sign.key")\nprint(sig)\n\n# Verify the signature of the file `LICENSE` using the public key `sign.crt`\nassert pysigning.verify(\'@LICENSE\', sig, key="sign.crt")\n```\n\n## License\n\nMIT\n\n## Contact\n\nA library by [Shawn Presser](https://www.shawwn.com). If you found it useful, please consider [joining my patreon](https://www.patreon.com/shawwn)!\n\nMy Twitter DMs are always open; you should [send me one](https://twitter.com/theshawwn)! It\'s the best way to reach me, and I\'m always happy to hear from you.\n\n- Twitter: [@theshawwn](https://twitter.com/theshawwn)\n- Patreon: [https://www.patreon.com/shawwn](https://www.patreon.com/shawwn)\n- HN: [sillysaurusx](https://news.ycombinator.com/threads?id=sillysaurusx)\n- Website: [shawwn.com](https://www.shawwn.com)\n\n',
    'author': 'Shawn Presser',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/shawwn/pysigning',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
