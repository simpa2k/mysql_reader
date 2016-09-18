import os

from formatters.MethodFormatter import MethodFormatter
from generators.angular.js.AngularJSGenerator import AngularJSGenerator


class AngularJSFactoryGenerator(AngularJSGenerator):

    def __init__(self, data, output_directory):
        super().__init__(data, output_directory)
        self.dependencies = ["$http", "$rootScope"]

    def construct_factory_name(self):
        return self.construct_uppercase_name("Service")

    def construct_stringified_dependencies(self):

        stringified_dependencies = ""

        first = True
        for dependency in self.dependencies:

            if first:
                first = False
            else:
                stringified_dependencies += ", "

            stringified_dependencies += "'{dependency}'".format(dependency=dependency)

        return stringified_dependencies

    def construct_dependencies(self):

        dependencies = ""

        first = True
        for dependency in self.dependencies:
            if first:
                first = False
            else:
                dependencies += ", "

            dependencies += dependency

        return dependencies

    def construct_promise(self):
        return "promise = $http.get({endpointName}).then(function(response) {{return response.data}});".format(endpointName=self.endpoint.retrieve_reference())

    def construct_get_function(self):
        return "get{uppercase_table_name}: function() {{if(!promise) {{{promise}}} return promise;}}".format(uppercase_table_name=self.construct_uppercase_name(""),
                                                                                                                promise=self.construct_promise())
    def construct_refresh_function(self):
        return "refresh{uppercase_table_name}: function() {{{promise}return promise;}}".format(uppercase_table_name=self.construct_uppercase_name(""),
                                                                                                  promise=self.construct_promise())
    def construct_factory_variable(self):
        service_variable = self.construct_lowercase_name("Service")
        return "var {service_variable} = {{{get_function},\n\t\t{refresh_function}}};return {service_variable};".format(service_variable=service_variable,
                                                                                                                      get_function=self.construct_get_function(),
                                                                                                                      refresh_function=self.construct_refresh_function())

    def generate(self):
        with open("generators/angular/js/templates/factory_template.txt", "r") as factory_template:
            data = factory_template.read()

            factory_name = self.construct_factory_name()
            stringified_dependencies = self.construct_stringified_dependencies()
            dependencies = self.construct_dependencies()
            factory_variable = self.construct_factory_variable()

            methodFormatter = MethodFormatter()
            factory_variable = methodFormatter.prettify(factory_variable)

            formatted_data = data.format(module_name=self.module_name,
                                         factory_name=factory_name,
                                         stringified_dependencies=stringified_dependencies,
                                         dependencies=dependencies,
                                         endpoint=self.endpoint.retrieve_definition(),
                                         factory_variable=factory_variable)

            os.makedirs(self.output_directory, exist_ok=True)

            with open(self.output_directory + self.construct_lowercase_name("-service.js"), "w") as output_file:
                output_file.write(formatted_data)