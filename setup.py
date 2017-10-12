from setuptools import setup

setup(
    # Application name:
    name="django_rest_guardian",

    # Version number (initial):
    version="1.1.0  ",

    # Application author details:
    author="Ankur Jain",
    author_email="ankurj630@gmail.com",

    # Packages
    packages=["django_rest_guardian"],
    # Include additional files into the package
    # include_package_data=True,
    url="https://github.com/droidlife/guardian",
    license="LICENSE",
    description='A django rest middleware which can be used on individual methods of APIViews. The middleware' +
                ' includes user authentication and payload verification',
    install_requires=['djangorestframework']
    # long_description=open("README.md").read(),
)
