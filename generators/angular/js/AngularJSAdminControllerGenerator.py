import os

from generators.angular.js.AngularJSGenerator import AngularJSGenerator
from generators.angular.js.JavaScriptFunction import JavaScriptFunction
from generators.angular.js.JavaScriptVariable import JavaScriptVariable
from readers.ForeignKey import ForeignKey


class AngularJSAdminControllerGenerator(AngularJSGenerator):

    def __init__(self, data, output_directory):

        super().__init__(data, output_directory)

        self.columns = data['columns']
        self.foreign_keys = data['foreign keys']

        self.dependencies = self.construct_dependencies()
        self.object_to_be_sent = self.construct_object_to_be_sent()

    def construct_object_to_be_sent(self):

        variable_name = "$scope.{table_name}ToBeSent".format(table_name=self.table_name)
        variable_value = "{}"

        return JavaScriptVariable(variable_name, variable_value)

    def construct_name(self):

        return "Admin" + self.construct_uppercase_name("Controller")

    def construct_dependencies(self):

        dependencies = "$scope, $rootScope, $http, $filter, SendObjectService"
        dependencies += ", " + self.construct_uppercase_name("Service")

        return dependencies

    def construct_foreign_object_variable(self, foreign_table):

        return "$scope.selected{foreign_table}".format(foreign_table=foreign_table.capitalize())

    def construct_get_foreign_key_object_functions(self):

        get_foreign_key_object_functions = []

        if self.foreign_keys is not None:

            for foreign_key in self.foreign_keys:

                foreign_table = foreign_key.foreign_table.capitalize()
                function_name = "var get{foreign_table}".format(foreign_table=foreign_table)

                foreign_object_list = "$scope.{endpoint_name}".format(endpoint_name=foreign_key.foreign_table)

                body_foreach_body = "{foreign_object_list}[value.{foreign_column}] = value;".\
                    format(foreign_object_list=foreign_object_list,
                           foreign_column=foreign_key.foreign_column)

                body_foreach = "angular.forEach(response.data, function(value) {{{foreach_body}}});".\
                    format(foreach_body=body_foreach_body)

                body_callback = "{foreign_object_list};{foreach}".format(foreign_object_list=foreign_object_list,
                                                                         foreach=body_foreach)

                body = "$http.get($rootScope.serverRoot + '{endpoint}').then(function(response) {{{body_callback}}})".\
                    format(endpoint=foreign_key.foreign_table,
                           body_callback=body_callback)

                get_foreign_key_object_functions.append(JavaScriptFunction(function_name, "", body))

        return get_foreign_key_object_functions

    def construct_select_foreign_key_object_functions(self):

        select_foreign_key_functions = []

        if self.foreign_keys is not None:

            for foreign_key in self.foreign_keys:

                foreign_table = foreign_key.foreign_table.capitalize()
                function_name = "var select{foreign_table}".format(foreign_table=foreign_table)

                body_if_statement_body = "{foreign_object_variable} = jQuery.extend({{}}, value);".\
                    format(foreign_object_variable=self.construct_foreign_object_variable(foreign_key.foreign_table))

                body_if_statement = "if(value.{foreign_table_pk} == {foreign_table_pk}) {{{body_if_statement_body}}}".\
                    format(foreign_table_pk=foreign_key.foreign_column,
                           parameter=self.table_name,
                           body_if_statement_body=body_if_statement_body)

                body_foreach = "angular.forEach($scope.{foreign_table}, function(value) {{{if_statement}}});".\
                    format(foreign_table=foreign_table,
                           if_statement=body_if_statement)

                function = JavaScriptFunction(function_name, self.table_name, body_foreach)
                function.add_useful_call_parameter(foreign_key.key)

                select_foreign_key_functions.append(function)

        return select_foreign_key_functions

    # Method to construct functions that send objects
    # that are considered representations of information
    # destined for a table that has a foreign key
    # relation to the table that the controller is modeled on.
    #
    # Only returns skeleton code at the moment, needs to be fleshed out.

    def construct_send_foreign_key_object_functions(self):

        send_foreign_key_object_functions = []

        if self.foreign_keys is not None:
            for foreign_key in self.foreign_keys:
                function_name = "var send{foreign_table}".format(foreign_table=foreign_key.foreign_table.capitalize())

                function = JavaScriptFunction(function_name, "", "")
                send_foreign_key_object_functions.append(function)

        return send_foreign_key_object_functions

    def construct_send_function_call(self, request_method):
        uppercase_table_name = self.construct_uppercase_name("")

        return "$scope.send{table_name} = $scope.{request_method}{table_name};".\
            format(table_name=uppercase_table_name,
                   request_method=request_method)

    def construct_set_put_state_function(self, select_foreign_key_object_functions):

        function_name = "$scope.setPutState"
        parameters = self.table_name

        body = ""

        for column in self.columns:
            body += "$scope.{table_name}ToBeSent.{column} = {table_name}.{column};".format(table_name=self.table_name,
                                                                                           column=column)
        for select_foreign_key_object_function in select_foreign_key_object_functions:

            call_parameter = self.table_name + "." + select_foreign_key_object_function.get_useful_call_parameter()
            body += select_foreign_key_object_function.get_function_call(call_parameter)

        body += self.construct_send_function_call("put")

        function = JavaScriptFunction(function_name, parameters, body)

        return function

    def construct_set_post_state_function(self):
        function_name = "$scope.setPostState"
        object_to_be_sent = self.object_to_be_sent.retrieve_definition()

        clear_foreign_objects = ""

        if self.foreign_keys is not None:
            for foreign_key in self.foreign_keys:
                clear_foreign_objects += "{foreign_object_variable} = undefined;".\
                    format(foreign_object_variable=self.construct_foreign_object_variable(foreign_key.foreign_table))

        send_gig_call = self.construct_send_function_call("post")
        body = object_to_be_sent + clear_foreign_objects + send_gig_call

        function = JavaScriptFunction(function_name, "", body)

        return function

    def construct_refresh_function(self):

        uppercase_table_name = self.construct_uppercase_name("")
        plural_table_name = self.construct_plural_name()

        function_name = "var refresh{table_name}".format(table_name=uppercase_table_name)
        body_callback = "$scope.{table_name_plural} = {table_name_plural};".\
            format(table_name_plural=plural_table_name)
        body = "{table_name}Service.refresh{table_name}().then(function({plural_table_name}){{{callback}}});".\
            format(table_name=uppercase_table_name,
                   plural_table_name=plural_table_name,
                   callback=body_callback)

        function = JavaScriptFunction(function_name, "", body)

        return function

    def construct_send_object_function(self, request_method, send_foreign_key_object_functions, refresh_function, state_changing_function=None):

        function_name = "$scope.{request_method}{table_name}".format(request_method=request_method,
                                                                     table_name=self.construct_uppercase_name(""))

        send_foreign_key_object_function_calls = "{calls}"
        calls = ""

        for send_foreign_key_object_function in send_foreign_key_object_functions:

            calls += send_foreign_key_object_function.get_function_call("")

        send_foreign_key_object_function_calls = send_foreign_key_object_function_calls.format(calls=calls)

        body_callback = refresh_function.get_function_call("")

        if state_changing_function is not None:
            body_callback += state_changing_function.get_function_call("")

        body = "{send_foreign_key_object_function_calls}SendObjectService.{request_method}Object({endpoint}, {object}, function() {{{callback}}});".\
            format(send_foreign_key_object_function_calls=send_foreign_key_object_function_calls,
                   request_method=request_method,
                   endpoint=self.endpoint.retrieve_reference(),
                   object=self.object_to_be_sent.retrieve_reference(),
                   callback=body_callback)

        function = JavaScriptFunction(function_name, "", body)

        return function

    def construct_request_functions(self, send_foreign_key_object_functions, refresh_function, state_changing_function):

        request_functions = {}

        if self.post:
            request_functions["post"] = self.construct_send_object_function("post",
                                                                         send_foreign_key_object_functions,
                                                                         refresh_function,
                                                                         state_changing_function)
        else:
            request_functions["post"] = JavaScriptFunction("", "", "")

        if self.put:
            request_functions["put"] = self.construct_send_object_function("put",
                                                                         send_foreign_key_object_functions,
                                                                         refresh_function)
        else:
            request_functions["put"] = JavaScriptFunction("", "", "")

        if self.delete:
            request_functions["delete"] = self.construct_send_object_function("delete",
                                                                         send_foreign_key_object_functions,
                                                                         refresh_function,
                                                                         state_changing_function)
        else:
            request_functions["delete"] = JavaScriptFunction("", "", "")

        return request_functions

    def generate(self):

        module_name = self.module_name
        controller_name = self.construct_name()
        dependencies = self.dependencies

        get_foreign_key_object_functions_list = self.construct_get_foreign_key_object_functions()
        select_foreign_key_object_functions_list = self.construct_select_foreign_key_object_functions()
        send_foreign_key_object_functions_list = self.construct_send_foreign_key_object_functions()

        get_foreign_key_object_functions = self.convert_function_list_to_string(get_foreign_key_object_functions_list)
        select_foreign_key_object_functions = self.convert_function_list_to_string(select_foreign_key_object_functions_list)
        send_foreign_key_object_functions = self.convert_function_list_to_string(send_foreign_key_object_functions_list)

        set_put_state_function = self.construct_set_put_state_function(select_foreign_key_object_functions_list)
        set_post_state_function = self.construct_set_post_state_function()

        refresh_function = self.construct_refresh_function()
        request_functions = self.construct_request_functions(send_foreign_key_object_functions_list,
                                                             refresh_function,
                                                             set_post_state_function)

        get_foreign_key_object_function_calls = ""

        for get_foreign_key_object_function in get_foreign_key_object_functions_list:
            get_foreign_key_object_function_calls += get_foreign_key_object_function.get_function_call(get_foreign_key_object_function.get_useful_call_parameter())

        with open("generators/angular/js/templates/admin_controller_template.txt", "r") as template:
            data = template.read()

            data = data.format(module_name=module_name,
                               controller_name=controller_name,
                               dependencies=dependencies,
                               get_foreign_key_object_functions=get_foreign_key_object_functions,
                               object_to_be_sent=self.object_to_be_sent.retrieve_definition(),
                               select_foreign_key_object_functions=select_foreign_key_object_functions,
                               set_put_state_function=set_put_state_function.retrieve(),
                               set_post_state_function=set_post_state_function.retrieve(),
                               send_foreign_key_object_functions=send_foreign_key_object_functions,
                               endpoint=self.endpoint.retrieve_definition(),
                               refresh_function=refresh_function.retrieve(),
                               post_object_function=request_functions["post"].retrieve(),
                               put_object_function=request_functions["put"].retrieve(),
                               delete_object_function=request_functions["delete"].retrieve(),
                               get_foreign_key_object_function_calls=get_foreign_key_object_function_calls,
                               set_state_function_call=set_post_state_function.get_function_call(set_post_state_function.get_useful_call_parameter())
                               )

            os.makedirs(self.output_directory, exist_ok=True)
            with open(self.output_directory + controller_name + ".js", "w") as output_file:
                output_file.write(data)