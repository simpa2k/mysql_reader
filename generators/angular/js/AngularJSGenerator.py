from generators.InputBasedGenerator import InputBasedGenerator


class AngularJSGenerator(InputBasedGenerator):

    def __init__(self, data, output_directory):
        super().__init__(data, output_directory)
        self.module_name = data['module name']

    def getEndpointName(self):
        return self.construct_lowercase_name("") + "Endpoint"

    def construct_endpoint(self):
        return "var {endpoint_name} = $rootScope.serverRoot + '{table_name}';".format(endpoint_name=self.getEndpointName(),
                                                                                      table_name=self.table_name)