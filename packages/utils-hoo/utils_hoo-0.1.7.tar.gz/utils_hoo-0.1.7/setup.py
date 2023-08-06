# -*- coding: utf-8 -*-

import sys

if 'bdist_wheel' in sys.argv:
    from setuptools import setup # to build wheel
else:
    from distutils.core import setup

with open('./readme.txt') as f:
    readme = f.read()

setup(name='utils_hoo',
      version='0.1.7',
      author='Genlovy Hoo',
      author_email='genlovhyy@163.com',
      url='https://github.com/Genlovy-Hoo/utils_hoo/', # 'www.genlovy.cn',
      # project_urls={
      #     'Source': 'https://github.com/Genlovy-Hoo/utils_hoo/tree/master'
      # },
      license='MPL 2.0',
      description="Genlovy Hoo's utils.",
      long_description=readme,
      # platform='any',
      packages=['utils_hoo',
                'utils_hoo.utils_logging',
                'utils_hoo.utils_plot',
                'utils_hoo.utils_datsci',
                'utils_hoo.utils_datsci.AHP',
                'utils_hoo.utils_datsci.ELM',
                'utils_hoo.utils_fin',
				'utils_hoo.utils_optimizer',
				'utils_hoo.utils_html',
                'utils_hoo.BackPacks',
                'utils_hoo.FindAddends',
                'utils_hoo.Sorts',
                'utils_hoo.tmp'])
