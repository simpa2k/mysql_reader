import os
from generators.Generator import Generator


class PhpBaseControllerGenerator(Generator):
    def __init__(self, output_directory):
        super().__init__(output_directory)

    def generate(self):
        with open('generators/php/templates/base_controller_template.txt') as base_controller_template:
            data = base_controller_template.read()

            os.makedirs(self.output_directory, exist_ok=True)
            with open(self.output_directory + 'BaseController.php', 'w') as base_controller_file:
                base_controller_file.write(data)
