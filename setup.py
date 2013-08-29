#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
from setuptools import setup

version = "0.2"

setup(
    name="django-twilio-sms",
    version=version,
    description="Twilio integration for SMS-based Django apps",
    license="MIT",

    author="Filip Wasilewski",
    author_email="en@ig.ma",

    url="https://github.com/nigma/django-twilio-sms",
    download_url="https://github.com/nigma/django-twilio-sms/zipball/master",

    long_description=open("README.rst").read(),

    package_dir={"django_twilio_sms": "src"},
    packages=["django_twilio_sms"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[
        "django",
        "djangorestframework>=2.3",
        "twilio>=3.5.1",
    ]
)
