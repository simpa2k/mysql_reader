import os
from generators.Generator import Generator


class PhpBaseModelGenerator(Generator):
    def __init__(self, output_directory):
        super().__init__(output_directory)
        
    def generate(self):
        with open('generators/php/templates/base_model_template.txt') as base_model_template:
            data = base_model_template.read()

            os.makedirs(self.output_directory, exist_ok=True)
            with open(self.output_directory + 'BaseModel.php', 'w') as base_model_file:
                base_model_file.write(data)
