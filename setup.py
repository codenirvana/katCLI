from setuptools import setup

setup(
  name='katcli',
  version='0.0.1',
  description='KAT CLI',
  long_description=open('README.rst').read(),
  author='Udit Vasu',
  author_email='admin@codenirvana.in',
  license='MIT',
  url='https://github.com/codenirvana/katCLI',
  packages=['katcli'],
  install_requires=[
    'ktorrent>=0.4.0',
    'click==6.2'
  ],
  entry_points={
    'console_scripts': [
        'katcli = katcli.katcli:main'
    ],
  }
)
