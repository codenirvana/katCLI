from setuptools import setup

setup(
    name='katcli',
    version='0.0.1',
    description='KAT Command line interface',
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
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords="kat torrent command line tool",
    entry_points={
        'console_scripts': [
            'katcli = katcli.katcli:main'
        ],
    }
)
