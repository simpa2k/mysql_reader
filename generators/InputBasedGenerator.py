from generators.Generator import Generator


class InputBasedGenerator(Generator):

    def __init__(self, data, output_directory):
        super().__init__(output_directory)
        self.table_name = data['table name']
        self.plural = data['plural']
        self.post = data['post']
        self.put = data['put']
        self.delete = data['delete']

    def construct_uppercase_name(self, suffix):
        lower_case_name = self.construct_lowercase_name(suffix)
        return lower_case_name[0].upper() + lower_case_name[1:]

    def construct_lowercase_name(self, suffix):
        plural_formatted_table_name = self.table_name + 's' if self.plural else self.table_name
        return plural_formatted_table_name + suffix