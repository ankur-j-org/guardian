# Guardian
> The middleware of the django-rest-framework on steroids.

# Overview
The guardian is highly flexible middleware for the django-rest. 

The current issue with the django-rest permission is that they are applied at class level and hence making it difficult to have seprarate permissions for individual methods. The guardian solves this issue by providing method based authentication.

Some reasons you might want to use Guardian:
* It can be used to *authenticate the user*
* It can be used to *verify the payload*
* Provides *method based authentications* as well as class based authentication.

# Requirements
* Python (2.x, 3.x)
* Django (1.8+)
* Django REST (3.x)

# Installation

Install using `pip`...

    pip install django-rest-guardian
