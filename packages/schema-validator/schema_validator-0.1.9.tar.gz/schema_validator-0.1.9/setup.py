# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schema_validator']

package_data = \
{'': ['*']}

install_requires = \
['flask>=2.0', 'humps', 'pydantic>=1.8']

setup_kwargs = {
    'name': 'schema-validator',
    'version': '0.1.9',
    'description': 'A flask extension to provide schema validation with pydantic.',
    'long_description': 'schema-validator\n============\n\n#### Generate from quart-schema\n\n\n### Install\n\n - `pip install schema-validator`\n\n### How to use\n\n```\n    from dataclasses import dataclass\n    from datetime import datetime\n    from typing import Optional\n    from pydantic import BaseModel\n\n    from flask import Flask\n    from schema_validator import FlaskSchema, validate\n\n    app = Flask(__name__)\n    \n    FlaskSchema(app)\n    \n    OR\n    \n    schema = FlaskSchema()\n    schema.init_app(app)\n\n    @dataclass\n    class Todo:\n        task: str\n        due: Optional[datetime]\n\n    class TodoResponse(BaseModel):\n        id: int\n        name: str\n\n    @app.post("/")\n    @validate(body=Todo, responses=TodoResponse)\n    def create_todo():\n        # balabala\n        return dict(id=1, name="2")\n        \n    @app.put("/")\n    @validate(\n        body=Todo,\n        responses={200: TodoResponse, 400: TodoResponse}\n    )\n    def update_todo():\n        # balabala\n        return TodoResponse(id=1, name="123")\n\n    @app.delete("/")\n    @validate(\n        body=Todo,\n        responses={200: TodoResponse}\n    )\n    def delete():\n        # balabala\n        return jsonify(id=1)\n     \n    @tags("SOME-TAG", "OTHER-TAG")\n    class View(MethodView):\n        @validate(...)\n        def get(self):\n            return {}\n       \n    app.cli.add_command(generate_schema_command)\n    \n    virtualenv:  flask schema swagger.json -> generate json swagger\n```\n\n\n##### FEATURES\n    - direct package/api/view_class name to export json-swagger\n    - direct tag to swagger html\n',
    'author': 'hs',
    'author_email': 'huangxiaohen2738@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/huangxiaohen2738/schema-validator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
