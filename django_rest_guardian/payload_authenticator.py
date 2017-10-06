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

    def __list_checker(self, validator, data):
        # Check if the passed data is list or not
        if type(data) != list:
            return False

        if len(validator) > 0:
            validator_type = validator[0]

            if type(validator_type) == list:
                is_checked = True

                # Check for every element in the data that it is list or not
                for element in data:
                    is_checked = self.__list_checker(validator[0], element) and is_checked

                return is_checked
            elif type(validator_type) == dict:
                is_checked = True

                # validate every dict in the list
                for element in data:
                    is_checked = is_checked and self.__dict_checker(validator_type, element)

                return is_checked
            else:
                # Check if type of every element is as specified in the validator
                for element in data:
                    if type(element) != validator_type:
                        return False

                return True
        else:
            return True

    def __dict_checker(self, validator, data):
        # check if passed data is dict or not
        if type(data) != dict:
            return False

        is_checked = True
        # check for each key in the validator
        for key in validator.keys():
            validator_type = validator[key]

            if type(validator_type) == list:
                is_checked = is_checked and self.__list_checker(validator_type, data[key])
            elif type(validator_type) == dict:
                is_checked = is_checked and self.__dict_checker(validator_type, data[key])
            elif type(validator_type) == type:
                is_checked = is_checked and isinstance(data[key], validator_type)
            else:
                is_checked = is_checked and validator_type == data[key]

        return is_checked

    def __type_enforcer(self, variable):
        # Check if the variable is simply list or dict without any further validations
        if type(self.payload[variable]) == type:
            return type(self.request_data[variable]) == self.payload[variable]
        elif type(self.payload[variable]) == list:
            # The variable has further validations on top of it being a list
            return self.__list_checker(self.payload[variable], self.request_data[variable])
        elif type(self.payload[variable]) == dict:
            # Further validate the dict
            return self.__dict_checker(self.payload[variable], self.request_data[variable])
        else:
            # Constant has been passed to check
            return self.request_data[variable] == self.payload[variable]

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
            elif self.current_method == 'POST' and self.__type_enforcer(variable):
                return True

            return False
