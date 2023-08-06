# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pd_aws_lambda', 'pd_aws_lambda.handlers']

package_data = \
{'': ['*']}

install_requires = \
['apig-wsgi>=2.0.0']

setup_kwargs = {
    'name': 'pd-aws-lambda',
    'version': '2.0.0',
    'description': 'Integrate your python applications with AWS Lambda and https://pythondeploy.co/.',
    'long_description': '===================================\nPython Deploy AWS Lambda Dispatcher\n===================================\n\n.. image:: https://badge.fury.io/py/pd-aws-lambda.svg\n    :target: https://badge.fury.io/py/pd-aws-lambda\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\nHandle AWS Lambda events.\n\nEvents are passed to handlers for processing.\nEach event is passed to the handler in this order:\n\n- Handler defined in the event\n- HTTP events handler (for WSGI applications)\n- SQS events handler (if configured)\n- Default handler (if configured)\n- Logger handler (if no default is defined)\n\nProvided Handlers\n-----------------\n\n- `pd_aws_lambda.handlers.wsgi.handler`: convert HttpAPI requests to WSGI environs.\n- `pd_aws_lambda.handlers.shell.handler`: Run shell commands.\n- `pd_aws_lambda.handlers.logger.handler`: log the received event and context.\n\nUsage\n-----\n\n1. Add `pd_aws_lambda` to your application dependencies.\n\n   .. code-block:: console\n\n    poetry add pd_aws_lambda\n\n2. Set the required environment variables according to your needs in your\n   `Python Deploy`_ application configuration.\n\n   .. code-block:: ini\n\n    # Python path to the WSGI application that will handle HTTP requests.\n    PD_WSGI_APPLICATION=my_django_project.wsgi.application\n\n    # Python path to the handler for SQS events.\n    PD_SQS_HANDLER=my_custom_handlers.sqs_handler\n\n    # Python path to the default fallback handler.\n    PD_DEFAULT_HANDLER=my_custom_handlers.default_handler\n\nCustom handlers\n---------------\n\nA handler is a python function that receives an `event` and a `context` and\ndoes something with them. It can return a value if it makes sense for the type\nof event. For example, HttpAPI handlers like the one we use to call your wsgi\napplication (`pd_aws_lambda.handlers.wsgi.handler`) should return a dictionary\ncompatible with the `AWS HttpAPI`_ to form an HTTP response.\n\n.. code-block:: python\n\n    def handler(event, context):\n        """\n        I handle AWS Lambda invocations.\n\n        I print the received event and context.\n        """\n        print("The event:", event)\n        print("The context:", context)\n\n----\n\n`Python Deploy`_\n\n.. _AWS HttpAPI: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html\n.. _Python Deploy: https://pythondeploy.co\n',
    'author': 'Federico Jaramillo Martínez',
    'author_email': 'federicojaramillom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pythondeploy/aws-lambda',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
