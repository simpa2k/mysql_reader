from abc import ABCMeta, abstractmethod
from .JsonGenerator import JsonGenerator

class MySqlGenerator(JsonGenerator):

    def __init__(self, json):
        super().__init__(json)
        
        self.table_name = json['name']
        self.fields = json['fields']
        self.primary_key = json['primary key']

        try:
            self.unique_key = json['unique key']
            self.foreign_key = json['foreign key']
        except KeyError:
            pass

    def construct_fields(self):
        fields = ''

        field_names = self.fields.keys()
        first = True
        for field_name in field_names:
            if first:
                first = False
            else:
                fields += ", "

            fields += (field_name + " " + self.fields[field_name])

        return fields 

    def construct_index(self, index_clause, indexed_columns):
        index_clause = ', ' + index_clause + '('
        first = True
        for indexed_column in indexed_columns:
            if first:
                first = False
            else:
                index_clause += ", "

            index_clause += indexed_column 
        index_clause += ')'

        return index_clause 


    def construct_primary_key(self):
        primary_key_clause = 'PRIMARY KEY'
        return self.construct_index(primary_key_clause, self.primary_key)


    def construct_unique_key(self):
        unique_key_clause = 'UNIQUE KEY'
        return self.construct_index(unique_key_clause, self.unique_key)

    def construct_foreign_keys(self):
        foreign_key_clause = ''

        for foreign_key in self.foreign_key:
            foreign_key_clause += ', FOREIGN KEY({0}) REFERENCES {1}'.format(foreign_key['key'], foreign_key['reference'])

        return foreign_key_clause 

    def generate(self):
        sql = "create table {0} (".format(self.table_name)
        
        sql += self.construct_fields()
        sql += self.construct_primary_key()

        try:
            sql += self.construct_unique_key()
        except AttributeError:
            pass

        try:
            sql += self.construct_foreign_keys()
        except AttributeError:
            pass

        sql += ");\n"

        with open('mysql/statements.txt', 'a') as statement_file:
            statement_file.write(sql)

