# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schema_validator']

package_data = \
{'': ['*']}

install_requires = \
['flask>=2.0', 'pydantic>=1.8', 'pyhumps>=1.6.1']

extras_require = \
{':python_version < "3.8"': ['typing_extensions']}

setup_kwargs = {
    'name': 'schema-validator',
    'version': '0.0.1',
    'description': 'A Flask extension to provide schema validation with pydantic',
    'long_description': 'Flask-Dantic-Schema\n============\n\n[![Build Status](https://app.travis-ci.com/huangxiaohen2738/flask-dantic-schema.svg?branch=main)](https://app.travis-ci.com/huangxiaohen2738/flask-dantic-schema)\n\n```\n    from dataclasses import dataclass\n    from datetime import datetime\n    from typing import Optional\n\n    from flask import Flask\n    from flask_dantic_schema import FlaskSchema, validate_request, validate_response\n\n    app = Flask(__name__)\n    FlaskSchema(app)\n\n    @dataclass\n    class Todo:\n        task: str\n        due: Optional[datetime]\n\n    @app.post("/")\n    @validate_request(Todo)\n    @validate_response(Todo, 201)\n    def create_todo(data: Todo) -> Todo:\n        ... # Do something with data, e.g. save to the DB\n        return data, 201\n```\n',
    'author': 'hs',
    'author_email': 'huangxiaohen2738@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https:/github.com/huangxiaohen2738/flask-dantic-schema',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
