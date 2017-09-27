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
            is_authenticated, result = UserAuthenticator(authenticators, request).authenticate()

            # if the result is not authenticated then return 401
            if not is_authenticated:
                return Response({
                    'message': 'user is not authorized to access the url'
                }, status=status.HTTP_401_UNAUTHORIZED)

            # The UserAuthenticator might return None because the user returned it. Hence to verify whether it was
            # returned by the user or by me i am using a null string.
            # Cause if the return is 'null' then the user does not changed the request object and hence it does not
            # need to be re assigned
            if type(result) is str and result == 'null':
                pass
            else:
                request = result

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
