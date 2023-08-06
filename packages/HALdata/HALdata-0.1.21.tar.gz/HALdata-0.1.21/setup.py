from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.1.21'
DESCRIPTION = 'Host to move data between Snowflake, S3 & Domo for SharkNinja HAL'

# Setting up
setup(
    name="HALdata",
    version=VERSION,
    author="cole Crescas",
    author_email="<colecrescas@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'json', 'botocore', 'snowflake.connector', 'boto3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)