from setuptools import setup

setup(
    name='python-amazon-ad-api',
    version='0.0.9',
    install_requires=[
        "requests",
        "six",
        "cachetools~=4.2.2",
        "pycryptodome",
        "python-dotenv",
        "pytz",
        "confuse",
    ],
    packages=['ad_api','ad_api.api','ad_api.auth','ad_api.base','ad_api.api.sp','ad_api.api.sb'],
    url='https://github.com/denisneuf/python-amazon-ad-api',
    license='MIT',
    author='Daniel',
    author_email='info@leadtech.es',
    description='Python wrapper for the Amazon Advertising API'
)