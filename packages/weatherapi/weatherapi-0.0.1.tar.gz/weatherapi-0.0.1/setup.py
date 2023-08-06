from setuptools import setup

setup(
    name='weatherapi',
    version='0.0.1',
    author='Martin Conur',
    author_email='martincontrerasur@gmail.com',
    packages=['weatherapi'],
    scripts=[],
    url='http://pypi.python.org/pypi/apiweather/',
    license='LICENSE.txt',
    description='weatherapi.com python access',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "requests >= 2.26.0"
    ],
)