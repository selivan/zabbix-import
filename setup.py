#!/usr/bin/env python3
from setuptools import setup

setup(
    name='zabbix-import',
    version=open('VERSION', 'r').read().strip(),
    url='https://github.com/selivan/zabbix-import',
    license='WTFPL',
    license_files = [ 'LICENSE' ],
    description='Utility to import Zabbix XML configuration: templates, hosts, host groups',
    long_description=open("README.md", 'r').read(),
    long_description_content_type='text/markdown',
    # twine requires author_email if author is set, but I don't like spam so homepage is enough
    author='Pavel Selivanov github.com/selivan',
    author_email='selivan.at.github@gmail-REMOVE-ANTI-SPAM.com',
    python_requires='>=2.5, >=3.0',
    install_requires=[],
    scripts=['zbx-import.py'],
    data_files=[('', ['LICENSE','VERSION','README.md'])],
)
