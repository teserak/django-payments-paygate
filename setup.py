#!/usr/bin/env python
from setuptools import setup


PACKAGES = [
    'payments_paygate',
]

REQUIREMENTS = [
    'Django>=1.6',
    'django-payments>=0.6.4',
]

setup(
    name='django-payments-paygate',
    author='William Wen',
    author_email='projects.wx@gmail.com',
    description='A django-payments backend for PayGate online payment (PayXML)',
    version='0.1',
    url='https://github.com/wenxinwilliam/django-payments-paygate.git',
    packages=PACKAGES,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    install_requires=REQUIREMENTS,
    zip_safe=False)
