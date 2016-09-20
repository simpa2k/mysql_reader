import os

from formatters.RequireJSFormatter import RequireJSFormatter
from generators.Generator import Generator


class AngularJSSendObjectServiceGenerator(Generator):

    def __init__(self, output_directory):
        super().__init__(output_directory)

    def generate(self):
        with open("generators/angular/js/templates/send_object_service_template.txt", "r") as template:
            data = template.read()

            require_js_formatter = RequireJSFormatter(data)
            data = require_js_formatter.format()

            os.makedirs(self.output_directory, exist_ok=True)
            with open(self.output_directory + "send-object-service.js", "w") as output_file:
                output_file.write(data)