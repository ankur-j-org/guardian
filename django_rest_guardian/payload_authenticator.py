'''
The file verifies the request payload.
'''


class PayloadAuthenticator:
    def __init__(self, payload, request):
        self.payload = payload
        self.request = request
        self.is_authenticated = True
        self.current_method = None
        self.request_data = None

    def authenticate(self):
        try:
            if not self.payload:
                return self.is_authenticated

            # using query params if the method is get
            if self.request.method == 'GET':
                self.current_method = 'GET'
                self.request_data = self.request.query_params
            else:
                self.current_method = 'POST'
                self.request_data = self.request.data

            self.__authenticator()
            return self.is_authenticated
        except:
            return False

    def __authenticator(self):
        for variable in self.payload:
            if variable not in self.request_data:
                self.is_authenticated = False
                break

            if not self.__type_verifier(variable):
                self.is_authenticated = False
                break

    def __type_verifier(self, variable):
        # if the variable is None then no need to check type
        if self.payload[variable] is None:
            return True

        # if the variable value is tuple then the data should be in the tuple
        elif type(self.payload[variable]) is tuple:
            return self.request_data[variable] in self.payload[variable]

        else:
            # checking the type of the variable if it matches the data type
            if self.current_method == 'GET' \
                    and type(self.payload[variable](self.request_data[variable])) == self.payload[variable]:
                return True
            elif self.current_method == 'POST' and type(self.request_data[variable]) == self.payload[variable]:
                return True

            return False
