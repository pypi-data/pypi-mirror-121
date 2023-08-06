#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='miidl',
    version='0.0.5',
    description='A Python package for microbial biomarkers identification powered by interpretable deep learning',
    url='https://github.com/chunribu/miidl/',
    author='chunribu',
    author_email='chunribu@mail.sdu.edu.cn',
    packages=find_packages(),
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "torch",
        "torchvision",
        "pandas",
        "captum",
        "scikit-learn",
    ],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='biomarker interpretable deeplearning',
    entry_points={
        'console_scripts': [
            # 'miidl = miidl:run_as_command',
            ]
    }
)