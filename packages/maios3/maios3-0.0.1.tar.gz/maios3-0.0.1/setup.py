from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Async file uploader to aws s3"
LONG_DESCRIPTION = "Async file uploader to aws s3 on top of aiobotocore"

# Setting up
setup(
    name="maios3",
    version=VERSION,
    author="MojixCoder",
    author_email="mojixcoder@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),

    install_requires=[
        "aiobotocore==1.4.1",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Environment :: Web Environment",
        "Development Status :: 3 - Alpha",
        "Framework :: AsyncIO",
    ]
)
