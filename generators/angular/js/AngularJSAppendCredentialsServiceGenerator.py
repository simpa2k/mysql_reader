import os

from generators.Generator import Generator
from generators.angular.js.AngularJSGenerator import AngularJSGenerator


class AngularJSAppendCredentialsServiceGenerator(Generator):

    def __init__(self, output_directory):
        super().__init__(output_directory)

    def generate(self):
        with open("generators/angular/js/templates/append_credentials_service_template.txt", "r") as template:
            data = template.read()

            os.makedirs(self.output_directory, exist_ok=True)
            with open(self.output_directory + "append-credentials-service.js", "w") as output_file:
                output_file.write(data)