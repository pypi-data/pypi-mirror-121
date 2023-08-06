#!/usr/bin/env python
"""Factorial project"""
from setuptools import find_packages, setup

setup(name = 'Warframepip',
    version = '1.0',
    description = "Warframe Modules. WORK IN PROGRESS!",
    long_description = "Very heavy project for near future. Once finish i hope many people will use this.\nI am Accepting Contributers",
    platforms = ["Linux", "Windows", "MacOS"],
    author="Blake Thompson",
    author_email="blakethompsonbat@gmail.com",
    url="http://pymbook.readthedocs.org/en/latest/",
    license = "MIT",
    packages=['Warframepip'],
    install_requires=['python-dotenv', 'requests', 'discord.py']
    )