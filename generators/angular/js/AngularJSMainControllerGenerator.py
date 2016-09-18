import os

from formatters.MethodFormatter import MethodFormatter
from generators.Generator import Generator


class AngularJSMainControllerGenerator(Generator):

    def __init__(self, tables, output_directory):
        super().__init__(output_directory)
        self.tables = tables
        self.module_name = tables[0]['module name']

    def extract_table_name(self, table):
        return table['table name']

    def capitalize_table_name(self, table):

        return self.extract_table_name(table).capitalize()

    def construct_dependencies(self):
        dependencies = "$scope, $rootScope, $http"

        for table in self.tables:
            dependencies += ", {uppercase_table_name}Service".format(uppercase_table_name=self.capitalize_table_name(table))

        return dependencies

    def plural_format_table_name(self, table):

        table_name = self.extract_table_name(table)

        return table_name + 's' if table['plural'] else table_name

    def construct_get_data_functions(self):

        get_data_functions = ""

        for table in self.tables:

            plural_formatted_table_name = self.plural_format_table_name(table)

            callback = "$scope.{table_name} = {table_name};".format(table_name=plural_formatted_table_name)
            function_call = "{uppercase_table_name}Service.get{uppercase_table_name}.then(function({table_name}) {{{callback}}});".\
                format(uppercase_table_name=self.capitalize_table_name(table),
                       table_name=plural_formatted_table_name,
                       callback=callback)

            get_data_functions += function_call

        return get_data_functions

    def generate(self):

        dependencies = self.construct_dependencies()
        get_data_functions = self.construct_get_data_functions()

        with open("generators/angular/js/templates/main_controller_template.txt", "r") as template:
            data = template.read()

            method_formatter = MethodFormatter()
            get_data_functions = method_formatter.prettify(get_data_functions)

            data = data.format(module_name=self.module_name,
                               dependencies=dependencies,
                               get_data_functions=get_data_functions)

            os.makedirs(self.output_directory, exist_ok=True)
            with open(self.output_directory + "MainController.js", "w") as output_file:
                output_file.write(data)