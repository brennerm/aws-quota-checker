from setuptools import setup, find_packages

setup(
    name='aws-quota-checker',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'click',
        'tabulate'
    ],
    extras_require={
        'dev':{
            'autopep8',
            'pylint',
            'keepachangelog',
            'wheel'
        }
    },
    entry_points='''
        [console_scripts]
        aws-quota-checker=aws_quota.cli:cli
    ''',
)