from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aws-quota-checker',
    version='1.6.0',
    description='A CLI tool that checks your AWS quota utilization',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'click',
        'tabulate',
        'cachetools'
    ],
    extras_require={
        'dev':{
            'autopep8',
            'pylint',
            'keepachangelog',
            'wheel'
        },
        'prometheus':{
            'prometheus-client'
        }
    },
    entry_points='''
        [console_scripts]
        aws-quota-checker=aws_quota.cli:cli
    ''',
)
