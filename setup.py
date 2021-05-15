#!/usr/bin/env python

from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="init-args-serializer",
    version="1.1",
    description="Python serializer based on init-args",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Xfel/init-args-serializer",
    author="Felix Treede",
    author_email="felixtreede@yahoo.de",
    packages=find_packages(include=["init_args_serializer"], exclude=["tests"]),
    python_requires=">=3.7, <4",
    install_requires=[],
    extras_require={"test": ["pytest", "pytest-cov"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="serialization, serializer, init-args",
)
