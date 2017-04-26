"""PIP Project Installation Program."""

from setuptools import setup, find_packages
from lets_do_dns import __version__

setup(
    name='lets-do-dns',
    version=__version__,
    license='Apache-2.0',
    author='Joel Gerber',
    author_email='joel@grrbrr.ca',
    url='https://github.com/jitsusama/lets-do-dns',
    download_url=(
        'https://github.com/jitsusama/lets-do-dns/archive/%s.tar.gz' % (
            __version__)),
    keywords=['certbot', 'letsencrypt', 'DigitalOcean', 'DNS', 'SSL'],
    description=(
        "A letsencrypt certbot auth/cleanup hook program engineered to "
        "handle hostname ownership authentication via DigitalOcean's DNS "
        "system."),
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lets-do-dns = lets_do_dns.__main__:main'
        ]
    },
    install_requires=['requests'],
    tests_requires=[
        'pylama',
        'pylama_pylint',
        'pytest',
        'pytest-cov',
        'pytest-mock',
        'requests',
    ]
)
