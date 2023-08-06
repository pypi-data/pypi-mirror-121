# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alarmer', 'alarmer.provider']

package_data = \
{'': ['*']}

install_requires = \
['better-exceptions']

setup_kwargs = {
    'name': 'alarmer',
    'version': '0.1.1',
    'description': 'A tool focus on error reporting for your application',
    'long_description': '# alarmer\n\n[![image](https://img.shields.io/pypi/v/alarmer.svg?style=flat)](https://pypi.python.org/pypi/alarmer)\n[![image](https://img.shields.io/github/license/tortoise/alarmer)](https://github.com/tortoise/alarmer)\n[![pypi](https://github.com/long2ice/alarmer/actions/workflows/pypi.yml/badge.svg)](https://github.com/long2ice/alarmer/actions/workflows/pypi.yml)\n[![ci](https://github.com/long2ice/alarmer/actions/workflows/ci.yml/badge.svg)](https://github.com/long2ice/alarmer/actions/workflows/ci.yml)\n\n`Alarmer` is a tool focus on error reporting for your application.\n\n## Installation\n\n```shell\npip install alarmer\n```\n\n## Usage\n\nIt\'s simple to integrate `alarmer` in your application, just call `Alarmer.init` on startup of your application.\n\n```py\nimport os\n\nfrom alarmer import Alarmer\nfrom alarmer.provider.feishu import FeiShuProvider\n\n\ndef main():\n    Alarmer.init(providers=[FeiShuProvider(webhook_url=os.getenv("FEI_SHU_WEBHOOK_URL"))])\n    raise Exception("test")\n\n\nif __name__ == "__main__":\n    main()\n```\n\n### Intercept Error Logging\n\nIf you want to intercept the `ERROR` level logging, you can use `LoggingHandler`.\n\n```py\nimport logging\nimport os\n\nfrom alarmer import Alarmer\nfrom alarmer.log import LoggingHandler\nfrom alarmer.provider.feishu import FeiShuProvider\n\n\ndef main():\n    Alarmer.init(providers=[FeiShuProvider(webhook_url=os.getenv("FEI_SHU_WEBHOOK_URL"))])\n    logging.basicConfig(\n        level=logging.INFO,\n    )\n    logger = logging.getLogger()\n    logger.addHandler(LoggingHandler())\n    logging.error("test logging")\n\n\nif __name__ == "__main__":\n    main()\n\n```\n\nNow when you run the script, you will receive the errors in your provider.\n\n## Provider\n\nYou can set number of providers for error reporting. All kinds of providers can be found\nin [providers](./alarmer/provider).\n\n- Email\n- [FeiShu](https://www.feishu.cn/hc/zh-CN/articles/360024984973)\n- [WeCom](https://work.weixin.qq.com/api/doc/90000/90136/91770)\n\n### Custom Provider\n\nYou can write your own custom provider by inheriting the `Provider` class.\n\n```py\nimport smtplib\nfrom typing import List\n\nfrom alarmer.provider import Provider\n\n\nclass EmailProvider(Provider):\n    def __init__(self, host: str, port: int, from_addr: str, to_addrs: List[str], **kwargs):\n        super().__init__()\n        self.smtp = smtplib.SMTP(host=host, port=port)\n        self.from_addr = from_addr\n        self.to_addrs = to_addrs\n        self.kwargs = kwargs\n\n    def send(self, message: str):\n        self.smtp.sendmail(\n            from_addr=self.from_addr, to_addrs=self.to_addrs, msg=message, **self.kwargs\n        )\n```\n\n## Throttling\n\n`Throttling` is used to throttle error messages.\n\n```py\nfrom alarmer import Alarmer\nfrom alarmer.throttling import Throttling\n\nAlarmer.init(global_throttling=Throttling(), providers=[...])\n```\n\n### Custom Throttling\n\nYou can write your own throttling by inheriting the `Throttling` class.\n\n```py\nimport abc\nimport threading\nimport time\nimport typing\n\nif typing.TYPE_CHECKING:\n    from alarmer import Provider\n\n\nclass Throttling(abc.ABC):\n    def __init__(self):\n        self.last_time = time.time()\n        self.lock = threading.Lock()\n\n    def __call__(self, provider: "Provider", exc, value, tb) -> bool:\n        with self.lock:\n            if time.time() - self.last_time < 1:\n                return False\n            self.last_time = time.time()\n            return True\n\n```\n\n## License\n\nThis project is licensed under the\n[Apache-2.0](https://github.com/long2ice/alarmer/blob/master/LICENSE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/alarmer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
