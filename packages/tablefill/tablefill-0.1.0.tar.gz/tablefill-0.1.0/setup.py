# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tablefill']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=8.14.0,<9.0.0',
 'typer>=0.4.0,<0.5.0',
 'xlrd==1.2.0',
 'xlutils>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['fill = tablefill.cli:app']}

setup_kwargs = {
    'name': 'tablefill',
    'version': '0.1.0',
    'description': 'Excel模板数据填充,快速应对Web项目数据导入',
    'long_description': '# 背景\n在测试Web后台管理系统项目时,导入数据是个高频出现的功能,[tablefill](https://github.com/zy7y/tablefill)主要完成根据配置文件对模板进行填充数据\n\n# ',
    'author': '柒意',
    'author_email': '396667207@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitee.com/zy7y/tablefill',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
