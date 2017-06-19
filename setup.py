from setuptools import setup

setup(
  name='rollback',
  version='0.1',
  author='Mika Lackman',
  author_email='mika.lackman@gmail.com',
  scripts=['bin/rollback.py'],
  install_requires=[
    'boto3',
    'click'
  ]
)
