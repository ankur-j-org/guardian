from payload_authenticator import PayloadAuthenticator
from user_authenticator import UserAuthenticator
from rest_framework import status
from rest_framework.response import Response


def guardian(*authenticators, **payload):
    def authenticate(func):
        def wrap(context, request):
            is_authenticated, result = UserAuthenticator(authenticators, request).authenticate()

            if not is_authenticated:
                return Response({
                    'message': 'user is not authorized to access the url'
                }, status=status.HTTP_401_UNAUTHORIZED)

            if result:
                request = result

            if PayloadAuthenticator(payload, request).authenticate():
                return func(context, request)
            else:
                return Response({
                    'message': 'invalid payload'
                }, status=status.HTTP_400_BAD_REQUEST)

        wrap.__name__ = func.__name__
        return wrap

    return authenticate
