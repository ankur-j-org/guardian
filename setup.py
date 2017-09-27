from setuptools import setup

setup(
    # Application name:
    name="django_rest_guardian",

    # Version number (initial):
    version="1.0.0",

    # Application author details:
    author="Ankur Jain",
    author_email="ankurj630@gmail.com",

    # Packages
    packages=["django_rest_guardian"],

    # Include additional files into the package
    # include_package_data=True,

    # Details
    url="https://github.com/droidlife/guardian",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",
    install_requires=['djangorestframework']

    # long_description=open("README.txt").read(),
)
