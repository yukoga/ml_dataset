# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='ml_dataset',
      version='0.0.1',
      description='Module works for access to public data, some databases, and API\'s.',
      license='no',
      author='yukoga',
      author_email='yukoga@gmail.com',
      url='https://github.com/yukoga/ml_dataset.git',
      packages=['ml'],
      install_requires = open('requirements.txt').read().splitlines(),
      classifiers=[
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.5',
          'Intended Audience :: Developers',
          'Topic :: Utilities',
          'License :: unkown',
          'Operating System :: OS Independent',
      ]
     )