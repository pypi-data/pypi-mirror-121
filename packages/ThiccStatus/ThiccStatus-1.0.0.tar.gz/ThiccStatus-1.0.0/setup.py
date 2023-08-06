from setuptools import setup, find_packages

setup(
    name='ThiccStatus',
    version='1.0.0',
    lisence='Apache Version 2.0',
    description='Discord module for ThiccStatus.',
    long_description=open("README.md", "r").read(),
    long_description_content_type='text/markdown',
    url='https://isthicc.dev/',
    author='IsThicc Software',
    packages=find_packages(),
    install_requires=['discord','aiohttp']
)
