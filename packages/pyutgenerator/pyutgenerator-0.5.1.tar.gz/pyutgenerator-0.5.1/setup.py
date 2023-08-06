# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyutgenerator']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pyutgen = pyutgenerator.run:main']}

setup_kwargs = {
    'name': 'pyutgenerator',
    'version': '0.5.1',
    'description': 'python ut test code generator.',
    'long_description': '#  Python UT generator\nThis tools generate automatically Python pytest Unit test code.  \nThis project uses ast module to generate.  \nEasy to make coverage test.\n\n### feature\n\n* Generate unit test python file in tests package.\n* Generate pytest test function from each function.\n* Generate mock patch syntax code.\n* Generate argument syntax code to call.\n* if function has return value, create assert return.\n\n## Installation\n\n### install pip\n\n```\npip install pyutgenerator\n```\nhttps://pypi.org/project/pyutgenerator/\n\n\n## Run tool.\n\n### genarete test code\n\n\n```\npyutgen "Input File Name"\n```\n\n\n### sample input file\n\n```\nimport os\n\n\ndef aaaaa():\n    """\n    call and return\n    """\n    return os.path.exists(\'\')\n\n```\n\n### sample out put\n\n```\n\nimport pytest\nfrom unittest.mock import patch\nfrom unittest.mock import MagicMock\n\nfrom tests.pyutgenerator.data import pattern01\n\ndef test_aaaaa():\n    # plan\n\n    # do\n    with\\\n            patch(\'tests.pyutgenerator.data.pattern01.os.path\') as m1:\n        m1.return_value = None\n        m1.exists = MagicMock(return_value=None)\n        ret = pattern01.aaaaa()\n\n        # check\n        assert ret\n\n```\n### for future\n\n* regist pypi.\n* customize parameter options.\n* parameter type for str,list, obj ...\n* write return_value.\n* exception check.\n* call default and pass test.\n* genarete various parameters for test.\n* web ui for test.\n\n### Prerequisites\n\nnot yet\n\n```\nnot yet\n```\n\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details\n\n## Acknowledgments\n\n* Hat tip to anyone whose code was used\n* Inspiration\n* etc\n',
    'author': 'shigeshige',
    'author_email': '5540474+shigeshige@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shigeshige/py-ut-generator',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
