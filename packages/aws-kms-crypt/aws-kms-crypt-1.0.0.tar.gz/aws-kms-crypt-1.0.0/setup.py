# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kmscrypt']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['boto3<2', 'cryptography>=3.4,<4.0']

setup_kwargs = {
    'name': 'aws-kms-crypt',
    'version': '1.0.0',
    'description': 'Utility for encrypting and decrypting secrets with the AWS KMS service',
    'long_description': 'Utility for encrypting and decrypting secrets with the AWS KMS service.\n\n# Installation\n\nInstall from PyPI with pip\n\n```bash\npip install aws-kms-crypt\n```\n\n# Usage\n\nRequires Python 3.6 or newer.\n\n```python\nimport kmscrypt\n\n# Encrypting Data\n>>> result = kmscrypt.encrypt(\'secretp4ssw0rd!\', key_id=\'alias/common\', encryption_context={\n...     \'purpose\': \'automation\'\n... })\n>>> result\n{\n    "EncryptedDataKey": "AQIDAHhyrbU/fPcQ+a8pJiYC<snip>",\n    "Iv": "689806fe9d571afeffa4c7c24247c766",\n    "EncryptedData": "YRjZDQ2KzcEAZqUy7SpWWA==",\n    "EncryptionContext": {\n        "purpose": "automation"\n    }\n}\n\n# Decrypting data\n>>> kmscrypt.decrypt(result)\nb\'secretp4ssw0rd!\'\n```\n\n# Changelog\n\n## v1.0.0 (2021-09-25)\n\n* Dropped Python 2.7 support.\n* Replaced [pycrypto](https://www.dlitz.net/software/pycrypto/) with [cryptography](https://cryptography.io/en/latest/).\n\n# License\n\nMIT',
    'author': 'Sami Jaktholm',
    'author_email': 'sjakthol@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
