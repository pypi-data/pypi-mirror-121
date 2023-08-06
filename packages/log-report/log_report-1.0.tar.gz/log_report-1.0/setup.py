from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='log_report',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    author="ME IS ME WHO ELSE",
    install_requires=[
          'markdown',
          'argparse'
      ]
)