try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A sweet little python assembler which assembles output from dis to python bytecode',
    'author': 'Krishna Ram Prakash R',
    'url': 'https://github.com/rkrp/payasm',
    'download_url': 'https://github.com/rkrp/payasm',
    'author_email': 'krp@gtux.in',
    'version': '0.1',
    'install_requires': [],
    'packages': ['payasm'],
    'scripts': ['bin/payasm'],
    'name': 'payasm',
    'license' : 'GPLv3',
    'classifiers' : [
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
    ],
}

setup(**config)

