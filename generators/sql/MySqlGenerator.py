import os
from generators.Generator import Generator


class MySqlGenerator(Generator):
    def __init__(self, table, output_directory):

        super().__init__(output_directory)
        self.table_name = table['table name']
        self.fields = table['columns']
        self.primary_key = table['primary key']
        self.unique_key = table['unique key']
        self.foreign_key = table['foreign keys']

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
            foreign_key_clause += ', FOREIGN KEY({0}) REFERENCES {1}'.format(foreign_key.key, foreign_key.reference)

        return foreign_key_clause

    def generate(self):
        sql = "create table {0} (".format(self.table_name)

        sql += self.construct_fields()
        sql += self.construct_primary_key()

        if self.unique_key is not None:
            sql += self.construct_unique_key()

        if self.foreign_key is not None:
            sql += self.construct_foreign_keys()

        sql += ");\n"

        os.makedirs('mysql', exist_ok=True)
        with open('mysql/statements.sql', 'a') as statement_file:
            statement_file.write(sql)
