'''
The file authenticates the user depending on the guard method implemented by the user.
'''

import inspect


class UserAuthenticator(object):
    def __init__(self, authenticators, request):
        self.authenticator_list = authenticators
        self.is_authenticated = False
        self.request = request
        self.result = 'null'

    def authenticate(self):
        # if there is no authenticators return True
        if not self.authenticator_list:
            self.is_authenticated = True
            return self.is_authenticated

        for authenticator in self.authenticator_list:

            # Expecting authenticators to be of class type
            if not inspect.isclass(authenticator):
                return TypeError('Expected {0} to be of type class'.format(authenticator.__name__))

            # Expecting authenticator class to have implemented the guard method
            if not hasattr(authenticator, 'guard'):
                raise NotImplementedError('Guard method is not implemented in {0} class'.format(authenticator.__name__))

            # calling the guard method with request parameter
            response = authenticator().guard(self.request)

            # if the response is only boolean then check the response.
            # If its true then the user is verified
            if type(response) is bool:
                if response:
                    self.is_authenticated = True
                    break
            else:
                raise TypeError('Unexpected return type from {0} class'.format(authenticator.__name__))
        return self.is_authenticated
