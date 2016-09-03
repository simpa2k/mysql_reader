import os 
from abc import ABCMeta, abstractmethod
from generators.PhpGenerator import PhpGenerator
from generators.PhpMethod import PhpMethod
from generators.MethodFormatter import MethodFormatter

class PhpModelGenerator(PhpGenerator):

    def __init__(self, table_name, plural, post, put, delete, foreign_key):
        super().__init__(table_name, plural, post, put, delete)
        self.foreign_key = foreign_key
        self.base_method_body = "$this->getDB->{operation}('" + self.table_name + "', {parameters});"
        self.construct_method_signatures_and_bodies()

    def list_foreign_tables(self):
       tables = self.table_name 
        
       for foreign_key in self.foreign_key:
           tables += ", {foreign_table}".format(foreign_table=foreign_key.foreign_table)

       return tables

    def list_foreign_references(self):
       references = "array({array_items})" 

       key_reference_pairs = ""
       first = True
       for index, foreign_key in enumerate(self.foreign_key):
           if first:
               first = False
           else:
               key_reference_pairs += ", "

           key_reference_pairs += "{index} => ('{key}', '{reference}')".format(index=index, key=foreign_key.key, reference=foreign_key.foreign_column)

       return references.format(array_items=key_reference_pairs)
       

    def construct_foreign_key(self):
       tables = self.list_foreign_tables() 
       key_reference_pairs = self.list_foreign_references()

       get_method_body = "$action = 'SELECT *';$table = '{joined_tables}';$joinCondition = {join_condition};return ".format(joined_tables=tables, join_condition=key_reference_pairs)
       get_method_body = get_method_body + self.base_method_body.format(operation="action", parameters="$action, $table, $joinCondition")

       return get_method_body

    def construct_get_method_bodies(self):
        if self.foreign_key != None:
            self.get_method_body = self.construct_foreign_key()
        else:
            get_method_body = self.base_method_body.split(';')[0]
            self.get_method_body = get_method_body.format(operation="get", parameters="$where") + "->results();"

    def construct_method_signatures_and_bodies(self):
        base_method_signature = "public function {operation}({parameters})"
        insert_operation = "insert"
        update_operation= "update"
        delete_operation = "delete"

        self.insert_method_signature = base_method_signature.format(operation=insert_operation, parameters="$fields")
        self.update_method_signature = base_method_signature.format(operation=update_operation, parameters="$primaryKey, $fields")
        self.delete_method_signature = base_method_signature.format(operation=delete_operation, parameters="$where")

        self.construct_get_method_bodies()
        self.get_method_signature = base_method_signature.format(operation="get", parameters="$where")

        self.insert_method_body = self.base_method_body.format(operation=insert_operation,
                                                          table_name=self.table_name, 
                                                          parameters="$fields") if self.post else self.unimplementedMethodPlaceholder

        self.update_method_body = self.base_method_body.format(operation=update_operation, 
                                                          table_name=self.table_name, 
                                                          parameters="$primaryKey, $fields") if self.put else self.unimplementedMethodPlaceholder

        self.delete_method_body = self.base_method_body.format(operation=delete_operation, 
                                                          table_name=self.table_name, 
                                                          parameters="$where") if self.delete else self.unimplementedMethodPlaceholder

    def generate(self):
        with open('generators/model_template.txt', 'r') as model_template:
            data = model_template.read()

            class_name = self.construct_name('Model')
            get_method = PhpMethod(self.get_method_signature, self.get_method_body)
            insert_method = PhpMethod(self.insert_method_signature, self.insert_method_body)
            update_method = PhpMethod(self.update_method_signature, self.update_method_body)
            delete_method = PhpMethod(self.delete_method_signature, self.delete_method_body)

            method_formatter = MethodFormatter()
            get_method = method_formatter.prettify(get_method.retrieve())
            insert_method = method_formatter.prettify(insert_method.retrieve())
            update_method = method_formatter.prettify(update_method.retrieve())
            delete_method = method_formatter.prettify(delete_method.retrieve())

            data = data.format(name=class_name, get_method=get_method, insert_method=insert_method, update_method=update_method, delete_method=delete_method)

            directory = 'php/models/'
            os.makedirs(directory, exist_ok=True)

            with open(directory + class_name + '.php', 'w') as model_file:
                model_file.write(data)

