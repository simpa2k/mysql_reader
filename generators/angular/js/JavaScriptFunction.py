from generators.MethodFormatter import MethodFormatter


class JavaScriptFunction():

    def __init__(self, function_name, parameters, function_body):
        self.function_name = function_name
        self.parameters = parameters
        self.function_body = function_body
        self.call_parameter = ""
        self.first_parameter = True

    def retrieve(self):
        function = "{name} = function({parameters}) {{{body}}}".format(name=self.function_name,
                                                                       parameters=self.parameters,
                                                                       body=self.function_body)

        formatter = MethodFormatter()
        function = formatter.prettify(function)

        return function

    def get_function_call(self, parameters):
        function_signature = self.function_name.split("=")[0]
        function_signature = function_signature.split(" ")[1]
        function_signature += "({parameters})".format(parameters=parameters)

        return function_signature

    def add_useful_call_parameter(self, parameter):

        if self.first_parameter == True:
            self.first_parameter = False
        else:
            self.call_parameter += ", "

        self.call_parameter += parameter

    def get_useful_call_parameter(self):
        return self.call_parameter