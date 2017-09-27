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
            return self.is_authenticated, self.result

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

            # if response is a tuple then the expectation are to be of form (True, request)
            elif type(response) is tuple:
                if len(response) > 2:
                    raise AssertionError('Too many values to unpack. ' +
                                         'Expected 2 found more from {0} class'.format(authenticator.__name__))
                if type(response[0]) is not bool:
                    raise TypeError('Expected boolean from {0} class'.format(authenticator.__name__))

                if response[0]:
                    self.is_authenticated = True
                    self.result = response[1]
                    # raising warning if the user return none in the request
                    if not response[1]:
                        raise Warning('Received null response from {0} class. This response will be passed to the '
                                      'view layer.'.format(authenticator.__name__))
                    break
            else:
                raise TypeError('Unexpected type return from {0} class'.format(authenticator.__name__))

        return self.is_authenticated, self.result
