#!/usr/bin/env python

from distutils.core import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='init-args-serializer',
    version='1.0',
    description='Python init-args based Serializer',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Felix Treede',
    author_email='felixtreede@yahoo.de',
    url='https://github.com/Xfel/init-args-serializer',
    packages=['init_args_serializer'],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
