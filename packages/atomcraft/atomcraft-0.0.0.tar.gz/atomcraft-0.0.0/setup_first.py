"""
setup.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from setuptools import setup

# Then, install molecular
setup(
    name='atomcraft',
    version='0.0.0',
    author='C. Lockhart',
    author_email='chris@lockhartlab.org',
    description='atomcraft',
    long_description='atomcraft',
    url="https://www.lockhartlab.org",
    packages=[
        'atomcraft',
    ],
    install_requires=None,
    include_package_data=True,
    zip_safe=True,
)
