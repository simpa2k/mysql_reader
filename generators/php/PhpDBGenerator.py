import os

from generators.Generator import Generator


class PhpDBGenerator(Generator):

    def generate(self):
        with open('generators/php/templates/db_template.txt') as db_template:
            data = db_template.read()

            os.makedirs(self.output_directory, exist_ok=True)
            with open(self.output_directory + 'DB.php', 'w') as db_file:
                db_file.write(data)