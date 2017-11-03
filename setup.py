from setuptools import setup

setup(
    name='Get Stack Overflow Posts',
    version='1.0',
    long_description=__doc__,
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask','rauth',]
)
