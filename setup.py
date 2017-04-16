"""PIP Project Installation Program."""

from setuptools import setup, find_packages

setup(
    name='lets-do-dns',
    version='0.1.0',
    license='Apache',
    author='Joel Gerber',
    author_email='joel@grrbrr.ca',
    description=("A letsencrypt certbot pre/post hook program engineered "
                 "to handle hostname ownership authentication via "
                 "DigitalOcean's DNS system."),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lets-do-dns = certbot_dns_auth.__main__:main'
        ]
    },
)
