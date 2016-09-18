import os

from formatters.MethodFormatter import MethodFormatter
from generators.php.PhpGenerator import PhpGenerator
from generators.php.PhpMethod import PhpMethod


class PhpControllerGenerator(PhpGenerator):

    def __init__(self, data, output_directory):
        super().__init__(data, output_directory)
        self.construct_method_signatures_and_bodies()

    def construct_put_method_body(self):
        column_variables = ""
        primary_key_variable = '$primaryKey = "'
        unset_statement = ""
        update_statement = "$this->getModel()->update($primaryKey, $request->parameters);"

        first = True
        for column in self.primary_key:
            column_variables += "${column} = $request->parameters['{column}'];".format(column=column)

            if first:
                first = False
            else:
                primary_key_variable += ", "
            primary_key_variable += "{column} = ${column}".format(column=column)

            unset_statement += "unset($request->parameters['{column}']);".format(column=column)

        primary_key_variable += '";'

        return column_variables + primary_key_variable + unset_statement + update_statement

    def construct_method_signatures_and_bodies(self):
        base_method_signature = "public function {request_type}($request)"

        self.post_method_signature = base_method_signature.format(request_type="post")
        self.put_method_signature = base_method_signature.format(request_type="put")
        self.delete_method_signature = base_method_signature.format(request_type="delete")

        self.post_method_body = "$this->getModel()->insert($request->parameters);" if self.post else self.unimplementedMethodPlaceholder
        self.put_method_body = self.construct_put_method_body() if self.put else self.unimplementedMethodPlaceholder
        self.delete_method_body = "$id = $this->filterParameters(array('id'), $request->parameters);$this->getModel()->delete($this->formatParameters($id));" if self.delete else self.unimplementedMethodPlaceholder

    def generate(self):
        with open('generators/php/templates/controller_template.txt', 'r') as controller_template:
            data = controller_template.read()

            class_name = self.construct_uppercase_name('Controller')
            post_method = PhpMethod(self.post_method_signature, self.post_method_body)
            put_method = PhpMethod(self.put_method_signature, self.put_method_body)
            delete_method = PhpMethod(self.delete_method_signature, self.delete_method_body)

            method_formatter = MethodFormatter()

            post_method = method_formatter.prettify(post_method.retrieve())
            put_method = method_formatter.prettify(put_method.retrieve())
            delete_method = method_formatter.prettify(delete_method.retrieve())

            data = data.format(table_name=self.table_name,
                               name=class_name,
                               post_method=post_method,
                               put_method=put_method,
                               delete_method=delete_method)

            os.makedirs(self.output_directory, exist_ok=True)

            with open(self.output_directory + class_name + '.php', 'w') as controller_file:
                controller_file.write(data)

