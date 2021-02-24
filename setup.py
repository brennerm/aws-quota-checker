from setuptools import setup, find_packages

setup(
    name='aws-quota-checker',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'click',
        'tabulate'
    ],
    extras_require={
        'dev':{
            'autopep8',
            'pylint'
        }
    },
    entry_points='''
        [console_scripts]
        aws-quota-checker=aws_quota.cli:cli
    ''',
)