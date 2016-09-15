from generators.angular.js.AngularJSGenerator import AngularJSGenerator
from generators.angular.js.JavaScriptFunction import JavaScriptFunction


class AngularJSAdminControllerGenerator(AngularJSGenerator):

    def __init__(self, data, output_directory):
        super().__init__(data, output_directory)
        self.columns = data['columns']
        self.dependencies = ["$scope", "$rootScope", "$http", "$filter", "SendObjectService"]

    def construct_name(self):
        return "Admin" + self.construct_uppercase_name("Controller")

    def construct_dependencies(self):
        return self.dependencies.append(self.construct_uppercase_name("Service"))

    def construct_object_to_be_sent(self):
        return "$scope.{table_name}ToBeSent = {{}}".format(table_name=self.table_name)

    def construct_set_put_state_function(self):
        function_name = "$scope.setPutState"
        parameters = self.table_name

        body = ""
        for column in self.columns:
            body += "$scope.{table_name}ToBeSent.{column} = {table_name}.{column};".format(table_name=self.table_name,
                                                                                           column=column)

        js_function = JavaScriptFunction(function_name, parameters, body)
        function = js_function.retrieve()

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
        set_put_state_function = self.construct_set_put_state_function()
