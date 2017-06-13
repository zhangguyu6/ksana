#-*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(
    name='ksana',
    version='0.0.2.2',
    description='A sample Python web framework',
    url='https://github.com/zhangguyu6/ksana',
    author='Guyu Zhang',
    author_email='zhangguyu6@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['test*']),
    install_requires=['httptools>=0.0.9',],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='sample web asyncio framework',
)