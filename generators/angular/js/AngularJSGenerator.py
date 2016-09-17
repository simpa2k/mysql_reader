from generators.InputBasedGenerator import InputBasedGenerator
from generators.angular.js.JavaScriptVariable import JavaScriptVariable


class AngularJSGenerator(InputBasedGenerator):

    def __init__(self, data, output_directory):
        super().__init__(data, output_directory)
        self.module_name = data['module name']
        self.endpoint = self.construct_endpoint()

    def getEndpointName(self):
        return self.construct_lowercase_name("") + "Endpoint"

    def construct_endpoint(self):

        variable_name = "var " + self.getEndpointName()
        variable_value = "$rootScope.serverRoot + '{table_name}'".format(table_name=self.construct_plural_name())
        variable = JavaScriptVariable(variable_name, variable_value)

        return variable
