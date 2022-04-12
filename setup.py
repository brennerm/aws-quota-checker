from pathlib import Path
from setuptools import setup, find_packages

readme_file = Path(__file__).parent.resolve() / 'README.md'
long_description = readme_file.read_text()

setup(
    name='aws-quota-checker',
    version='1.12.0',
    description='A CLI tool that checks your AWS quota utilization',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'backoff',
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
