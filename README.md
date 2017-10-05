# Guardian
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![PyPI version](https://badge.fury.io/py/django-rest-guardian.svg)](https://badge.fury.io/py/django-rest-guardian)
> The django-rest middleware on steroids.

# Overview
The guardian is highly flexible middleware for the django-rest class based views. 

The current issue with the django-rest permission is that they are applied at class level and hence making it difficult to have seprarate permissions for individual methods. The guardian solves this issue by providing method based authentication.

Some reasons you might want to use Guardian:
* It can be used to *authenticate the user*
* It can be used to *authorize the payload*
* Provides *method based authentications* as well as class based authentication.

# Requirements
* Python (2.x, 3.x)
* Django (1.8+)
* Django REST (3.x)

# Installation

Install using `pip`...

    pip install django-rest-guardian
    
# Example

Let's take a look at a quick example of using **guardian** to build a simple middleware for authenticating user and authorizing payload.

**1. User Authentication**

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
 
 The guardian uses a logical **short circut OR** on the both the authenticator class.
 
 `app/views.py`
 
 ```python
 class UserView(APIView):
    
    @guardian(UserAuthenticator, AdminAuthenticator) # returns 401 if the UserAuthenticator returns False
    def get(self, request):
        print 'The user is authenticated if you are seeing this message'
        
        return Response({'result': True}, status=status.HTTP_200_OK)
```

**2. Payload Authorization**
 
 The guardian can also be used to to authorize the payload sent by the frontend.
 Let's assume this is the payload sent by the frontend
 
 ```javascript
 {
    "id": 5,
    "name": "John",
    "hobbies": ["Footbal", "Fencing"]
 }
 
 ```
 
 Let's verify the payload
 
 `app/views.py`
 
 ```python
 class UserView(APIView):
    
    # returns 400 if the payload is invalid
    @guardian(id=int, name=unicode, hobbies=list) # we use unicode because python treats the string as unicode for data.
    def post(self, request):
        print 'The payload is correct if you are seeing this message'
        
        return Response({'result': True}, status=status.HTTP_200_OK)
```

Guardian also supports validating n-dimensional lists.

What To Write | What Happens
--- | ---
list | simply validates if payload is list
[] | works same as *list*
[ int ] | Validates that a list should contain only integers. *Here **int** can be replaced by any acceptable python data type, even list. See below.*
[[ unicode ]] | Validates that a list should contain only lists which should contain only unicode Strings. In simpler terms payload should contain two-dimensional list of Strings.
[[[[[[ int ]]]]]] | This, well...This validates for (count-no-of-square-brackets) dimensional list of integers. I think you get the point.

# More Stuff

**1. Both user authentication and payload verification**

We can use user auth and payload verification both at the same time
`app/views.py`

 
 ```python
 class UserView(APIView):
   
    @guardian(UserAuthenticator, AdminAuthenticator, id=int, name=unicode, hobbies=list)
    def post(self, request):
        print 'The user is authenticated and the payload is correct if you are seeing this message'
        
        return Response({'result': True}, status=status.HTTP_200_OK)
```
 
 
**2. Pass additional parameter with request**

We can pass additional parameter with request to views layer

`app/permission.py`

```python
from django_rest_guardian.permission import AuthPermission

class UserAuthenticator(AuthPermission):
    def guard(self, request):
        if request.user_type == 'user':
            request.user = 'simon' # adding <user> param to request and returning it.
            return True
        else:
            return False
```

Now we can access this parameter in view layer `app/views.py` 

 ```python
 class UserView(APIView):
   
    @guardian(UserAuthenticator)
    def post(self, request):
        print request.user # prints 'simon'
        
        return Response({'result': True}, status=status.HTTP_200_OK)
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
 
 
 
 
