import os

from generators.Generator import Generator


class PhpConfigGenerator(Generator):
    def __init__(self, config, output_directory):
        super().__init__(output_directory)
        self.host = config['host']
        self.username = config['username']
        self.password = config['password']
        self.db = config['db']

    def generate(self):
        with open('generators/php/templates/config_template.txt') as config_template:
            data = config_template.read()

            config_output_directory = self.output_directory + "classes/"
            os.makedirs(config_output_directory, exist_ok=True)
            with open( config_output_directory + 'Config.php', 'w') as config_file:
                config_file.write(data)

        with open('generators/php/templates/init_template.txt') as init_template:
            data = init_template.read()
            data = data.format(host=self.host, username=self.username, password=self.password, db=self.db)

            init_output_directory = self.output_directory + "core/"
            os.makedirs(init_output_directory, exist_ok=True)
            with open(init_output_directory + 'init.php', 'w') as init_file:
                init_file.write(data)
