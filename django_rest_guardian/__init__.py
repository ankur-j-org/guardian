from payload_authenticator import PayloadAuthenticator
from user_authenticator import UserAuthenticator
from rest_framework import status
from rest_framework.response import Response

'''
Guardian ..
'''


def guardian(*authenticators, **payload):
    def authenticate(func):
        def wrap(context, request):
            # gets the final authentication and request(if changed)
            is_authenticated = UserAuthenticator(authenticators, request).authenticate()

            # if the result is not authenticated then return 401
            if not is_authenticated:
                return Response({
                    'message': 'user is not authorized to access the url'
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Verifying the payload. If its verified then calling the view function else returning a 400
            if PayloadAuthenticator(payload, request).authenticate():
                return func(context, request)
            else:
                return Response({
                    'message': 'invalid payload'
                }, status=status.HTTP_400_BAD_REQUEST)

        wrap.__name__ = func.__name__
        return wrap

    return authenticate
