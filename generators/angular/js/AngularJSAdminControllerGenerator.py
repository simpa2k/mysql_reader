from generators.angular.js.AngularJSGenerator import AngularJSGenerator
from generators.angular.js.JavaScriptFunction import JavaScriptFunction
from readers.ForeignKey import ForeignKey


class AngularJSAdminControllerGenerator(AngularJSGenerator):

    def __init__(self, data, output_directory):

        super().__init__(data, output_directory)

        self.columns = data['columns']
        self.foreign_keys = data['foreign keys']

        self.dependencies = ["$scope", "$rootScope", "$http", "$filter", "SendObjectService"]

    def construct_name(self):

        return "Admin" + self.construct_uppercase_name("Controller")

    def construct_dependencies(self):

        return self.dependencies.append(self.construct_uppercase_name("Service"))

    def construct_object_to_be_sent(self):

        return "$scope.{table_name}ToBeSent = {{}}".format(table_name=self.table_name)

    def construct_select_foreign_key_object_functions(self, parameter):

        select_foreign_key_functions = []

        if self.foreign_keys is not None:

            for foreign_key in self.foreign_keys:

                foreign_table = foreign_key.foreign_table.capitalize()

                function_name = "var select{foreign_table}".format(foreign_table=foreign_table)
                body = "angular.forEach($scope.{foreign_table}, function(value) {{if(value.{foreign_table_pk} == {parameter}){{$scope.selected{foreign_table} = jQuery.extend({{}}, value);}}}});".format(foreign_table=foreign_table,
                                                                                                                                                                                                      foreign_table_pk=foreign_key.foreign_column,
                                                                                                                                                                                                      parameter=parameter)

                function = JavaScriptFunction(function_name, parameter, body)
                function.add_useful_call_parameter(foreign_key.key)

                select_foreign_key_functions.append(function)

        return select_foreign_key_functions

    def construct_set_put_state_function(self, select_foreign_key_object_functions):

        function_name = "$scope.setPutState"
        parameters = self.table_name

        body = ""

        for column in self.columns:
            body += "$scope.{table_name}ToBeSent.{column} = {table_name}.{column};".format(table_name=self.table_name,
                                                                                           column=column)
        for select_foreign_key_object_function in select_foreign_key_object_functions:

            call_parameter = self.table_name + "." + select_foreign_key_object_function.get_useful_call_parameter()
            body += select_foreign_key_object_function.get_function_call(call_parameter) + ";"

        body += "$scope.sendGig = $scope.putGig;"

        function = JavaScriptFunction(function_name, parameters, body)

        return function.retrieve()

    def construct_set_post_state_function(self):
        pass

    def construct_set_state_functions(self):
        pass

    def construct_refresh_function(self):
        pass

    def construct_make_request_function(self):
        pass

    def construct_send_object_function(self):
        pass

    def construct_request_functions(self):
        pass

    def generate(self):

        module_name = self.module_name
        controller_name = self.construct_name()
        dependencies = self.construct_dependencies()
        object_to_be_sent = self.construct_object_to_be_sent()
        select_foreign_key_object_functions = self.construct_select_foreign_key_object_functions(self.table_name)
        set_put_state_function = self.construct_set_put_state_function(select_foreign_key_object_functions)
        print(set_put_state_function)