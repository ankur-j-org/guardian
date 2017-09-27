from distutils.core import setup

setup(
    # Application name:
    name="guardian",

    # Version number (initial):
    version="1.0.0",

    # Application author details:
    author="Ankur Jain",
    author_email="ankurj630@gmail.com",

    # Packages
    packages=["guardian"],

    # Include additional files into the package
    # include_package_data=True,

    # Details
    url="http://droidlife.github.io/me",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",
    requires=['djangorestframework']

    # long_description=open("README.txt").read(),
)
