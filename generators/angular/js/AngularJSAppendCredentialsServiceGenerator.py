import os

from formatters.RequireJSFormatter import RequireJSFormatter
from generators.Generator import Generator
from generators.angular.js.AngularJSGenerator import AngularJSGenerator


class AngularJSAppendCredentialsServiceGenerator(Generator):

    def __init__(self, output_directory):
        super().__init__(output_directory)

    def generate(self):
        with open("generators/angular/js/templates/append_credentials_service_template.txt", "r") as template:
            data = template.read()

            require_js_formatter = RequireJSFormatter(data)
            data = require_js_formatter.format()

            os.makedirs(self.output_directory, exist_ok=True)
            with open(self.output_directory + "append-credentials-service.js", "w") as output_file:
                output_file.write(data)