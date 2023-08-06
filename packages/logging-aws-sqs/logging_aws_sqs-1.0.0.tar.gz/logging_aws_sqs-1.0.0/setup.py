from setuptools import setup

setup(
    name='logging_aws_sqs',
    version='1.0.0',
    license='GNU GPL-3.0',
    description='A Python logging handler to sends logs to AWS SQS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='abhinav-chittora',
    author_email='chittora.abhinav@googlemail.com',
    url='https://github.com/abhinav-chittora/logging_aws_sqs.git',
    keywords=['logging', 'aws', 'sqs', 'log'],
    packages=['logging_aws_sqs'],
    install_requires=['requests >= 2.6.0, < 3.0.0', 'requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: System :: Logging'
    ]
)
