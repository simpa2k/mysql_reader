import os

from formatters.MethodFormatter import MethodFormatter
from generators.php.PhpGenerator import PhpGenerator
from generators.php.PhpMethod import PhpMethod


class PhpModelGenerator(PhpGenerator):

    def __init__(self, data, output_directory):
        super().__init__(data, output_directory)
        self.foreign_keys = data['foreign keys']
        self.base_method_body = "return $this->getDB()->{operation}({parameters});"
        self.construct_method_signatures_and_bodies()

    def list_foreign_tables(self):
       tables = self.table_name 
        
       for foreign_key in self.foreign_keys:
           tables += ", {foreign_table}".format(foreign_table=foreign_key.foreign_table)

       return tables

    def list_foreign_references(self):
       references = "array({array_items})" 

       key_reference_pairs = ""
       first = True
       for index, foreign_key in enumerate(self.foreign_keys):
           if first:
               first = False
           else:
               key_reference_pairs += ", "

           key_reference_pairs += "{index} => array('{key}', '{reference}')".format(index=index, key=foreign_key.key, reference=foreign_key.foreign_column)

       return references.format(array_items=key_reference_pairs)
       

    def construct_foreign_key(self):
       tables = self.list_foreign_tables() 
       key_reference_pairs = self.list_foreign_references()

       preparatory_statements = "$action = 'SELECT *';$table = '{joined_tables}';$joinCondition = {join_condition};".format(joined_tables=tables, join_condition=key_reference_pairs)
       get_method_body = self.base_method_body.split(';')[0]
       get_method_body = preparatory_statements + get_method_body.format(operation="action", parameters="$action, $table, $where, $joinCondition") + "->results();"

       return get_method_body

    def construct_get_all_method(self):
        return "return $this->getDB()->getAll('{table_name}')->results();".format(table_name=self.table_name);

    def construct_get_method_bodies(self):
        self.get_all_method_body = self.construct_get_all_method()

        if self.foreign_keys is not None:
            self.get_method_body = self.construct_foreign_key()
        else:
            get_method_body = self.base_method_body.split(';')[0]
            self.get_method_body = get_method_body.format(operation="get", parameters="'" + self.table_name + "', $where") + "->results();"

    def construct_method_signatures_and_bodies(self):
        base_method_signature = "public function {operation}({parameters})"
        insert_operation = "insert"
        update_operation= "update"
        delete_operation = "delete"

        self.insert_method_signature = base_method_signature.format(operation=insert_operation, parameters="$fields")
        self.update_method_signature = base_method_signature.format(operation=update_operation, parameters="$primaryKey, $fields")
        self.delete_method_signature = base_method_signature.format(operation=delete_operation, parameters="$where")

        self.construct_get_method_bodies()

        if(self.foreign_keys is None):
            self.get_method_signature = base_method_signature.format(operation="get", parameters="$where")
        else:
            self.get_method_signature = base_method_signature.format(operation="get", parameters="$where = array()")

        self.get_all_method_signature = base_method_signature.format(operation="getAll", parameters="")

        self.insert_method_body = self.base_method_body.format(operation=insert_operation,
                                                          parameters="'" + self.table_name + "', $fields") if self.post else self.unimplementedMethodPlaceholder

        self.update_method_body = self.base_method_body.format(operation=update_operation, 
                                                          parameters="'" + self.table_name + "', $primaryKey, $fields") if self.put else self.unimplementedMethodPlaceholder

        self.delete_method_body = self.base_method_body.format(operation=delete_operation, 
                                                          parameters="'" + self.table_name + "', $where") if self.delete else self.unimplementedMethodPlaceholder

    def generate(self):
        with open('generators/php/templates/model_template.txt', 'r') as model_template:
            data = model_template.read()

            class_name = self.construct_uppercase_name('Model')
            get_method = PhpMethod(self.get_method_signature, self.get_method_body)
            get_all_method = PhpMethod(self.get_all_method_signature, self.get_all_method_body)
            insert_method = PhpMethod(self.insert_method_signature, self.insert_method_body)
            update_method = PhpMethod(self.update_method_signature, self.update_method_body)
            delete_method = PhpMethod(self.delete_method_signature, self.delete_method_body)

            method_formatter = MethodFormatter()
            get_method = method_formatter.prettify(get_method.retrieve())
            get_all_method = method_formatter.prettify(get_all_method.retrieve())
            insert_method = method_formatter.prettify(insert_method.retrieve())
            update_method = method_formatter.prettify(update_method.retrieve())
            delete_method = method_formatter.prettify(delete_method.retrieve())

            data = data.format(table_name=self.table_name,
                               name=class_name,
                               get_method=get_method,
                               get_all_method=get_all_method,
                               insert_method=insert_method,
                               update_method=update_method,
                               delete_method=delete_method)

            os.makedirs(self.output_directory, exist_ok=True)

            with open(self.output_directory + class_name + '.php', 'w') as model_file:
                model_file.write(data)

