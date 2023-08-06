# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['annhub_python',
 'annhub_python.core',
 'annhub_python.ml_lib',
 'annhub_python.model',
 'annhub_python.services']

package_data = \
{'': ['*']}

install_requires = \
['fastapi==0.68.1',
 'joblib==1.0.1',
 'loguru==0.4.0',
 'pydantic>=1.8.2,<2.0.0',
 'pytest==6.2.4',
 'requests==2.22.0',
 'uvicorn==0.11.1']

setup_kwargs = {
    'name': 'annhub-python',
    'version': '0.1.5',
    'description': 'Main backend module, which is used for developing web-app logic and deploying AI model.',
    'long_description': '# backend-module\n\nMain backend module, which is used for developing web-app logic and deploying AI model.\n\n# Usage - Phase 1\n**Step 1:** \nInstall and update [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).\n\n**Step 2:**\nPut the desired model into your app with the following path:\n```\nml\\model\\<model_name>\n```\n**Step 3:** \nConfig model name as an environment variable in **.env** file.\n\n**Step 4:**\nBuild and run docker\n```\n$ docker-compose build\n$ docker-compose up -d\n```\n\n# Usage - Phase 2\n\nWe develop a RESTful web controller into a reusable library between many AI models. With these functionalities: **Input model**, **Define data input**, **logging**, **exception handler**.\n\n## Installing\nDelivering and versioning as a [PyPi](https://pypi.org/) package.\nInstall and update using [pip](https://pip.pypa.io/en/stable/getting-started/):\n\n```\n$ pip install annhub-python\n```\n## A simple example\n```python\nfrom annhub_python import PyAnn\n\npyann = PyAnn()\n\n# Define the expected AI model\npyann.set_model("D:\\ARI\\ANSCENTER\\TrainedModel_c++.ann")\n\n# Define which model ID will be used\npyann.set_model_id(5122020)\n\n# Define the input corresponding to the choosen model\npyann.set_input_length(4)\n\nif __name__ == "__main__":\n    pyann.run(host = "0.0.0.0", port = 8080, debug = False)\n\n```\n\n## API \nThe library will product two APIs: **health checking**, **predicting** as well as a [Swagger UI](https://swagger.io/) for API documentation.\n```\nGET: /api/v1/health\nPOST: /api/v1/predict\n```\n![Swagger UI](https://raw.githubusercontent.com/ans-ari/annhub-python/master/figures/swagger.png)',
    'author': 'ARI Technology',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
