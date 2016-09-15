from generators.MethodFormatter import MethodFormatter


class JavaScriptFunction():

    def __init__(self, function_name, parameters, function_body):
        self.function_name = function_name
        self.parameters = parameters
        self.function_body = function_body

    def retrieve(self):
        function = "{name} = function({parameters}) {{{body}}}".format(name=self.function_name,
                                                                       parameters=self.parameters,
                                                                       body=self.function_body)

        formatter = MethodFormatter()
        function = formatter.prettify(function)

        return function