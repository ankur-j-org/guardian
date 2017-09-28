# Guardian
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![PyPI version](https://badge.fury.io/py/django-rest-guardian.svg)](https://badge.fury.io/py/django-rest-guardian)
> The django-rest middleware on steroids.

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
    
# Example

Let's take a look at a quick example of using **guardian** to build a simple middleware for authenticating user and verifying payload.

**User Authentication**

Create a Permssion class in your desired file eg: `app/permission.py` by inherinting the **permission** class from guardian module and overriding the **guard** method

```python
from django_rest_guardian.permission import AuthPermission

# The method gets request as params and need to return True or False depicting whether the user is verified or not.
class UserAuthenticator(AuthPermission):
    def guard(self, request):
        if request.user_type == 'user':
            return True
        else:
            return False
        
 ```

Let's use this permission in our view layer - `app/views.py`

```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.permission import UserAuthenticator
from django_rest_guardian import guardian

class UserView(APIView):
    
    @guardian(UserAuthenticator) # returns 401 if the UserAuthenticator returns False
    def get(self, request):
        print 'The user is authenticated if you are seeing this message'
        
        return Response({'result': True}, status=status.HTTP_200_OK)
```

We can also have multiple authenticator classes. So now let's create one more class and pass it to the guardian

`app/permission.py`

```python
from django_rest_guardian.permission import AuthPermission

class UserAuthenticator(AuthPermission):
    def guard(self, request):
        if request.user_type == 'user':
            return True
        else:
            return False
        
 class AdminAuthenticator(AuthPermission):
    def guard(self, request):
        if request.user_type == 'admin':
            return True
        else:
            return False
        
 ```
 
 The guardian uses a logical **short circut or** on the both the authenticator class.
 
 `app/views.py`
 
 ```python
 class UserView(APIView):
    
    @guardian(UserAuthenticator, AdminAuthenticator) # returns 401 if the UserAuthenticator returns False
    def get(self, request):
        print 'The user is authenticated if you are seeing this message'
        
        return Response({'result': True}, status=status.HTTP_200_OK)
```
 
 
 
 
 
 
 
 
 
 
 
 
