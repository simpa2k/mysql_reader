from abc import ABCMeta, abstractmethod
from .JsonGenerator import JsonGenerator

class PhpGenerator(JsonGenerator):
    
    def __init__(self, json):
        super().__init__(json)

        self.table_name = json['name']
        self.plural = json['plural']
        self.post = json['post']
        self.put = json['put']
        self.delete = json['delete']

    def evaluatesToTrue(self, string):
        return string == "true"

    def construct_controller_name(self):
        upper_case_table_name = self.table_name.capitalize()
        plural_formatted_table_name = upper_case_table_name + 's' if self.evaluatesToTrue(self.plural) else upper_case_table_name

        return plural_formatted_table_name + 'Controller'
    
    def generatePostMethod(self, template):
        method_body = "public function post($request) {{ {post_method} }}"

        if self.evaluatesToTrue(self.post):
            return method_body.format(post_method="$this->getModel()->insert($request->parameters);")
        else:
            return method_body.format(post_method="")


    def generatePutMethod(self, template):
        method_body = "public function put($request) {{ {put_method} }}"

        if self.evaluatesToTrue(self.put):
            return method_body.format(put_method="\n\t$id = $request->parameters['id'];\n\t$primaryKey = 'id = $id';\n\tunset($request->parameters['id']);\n\t$this->getModel()->update($primaryKey, $request->parameters);")
        else:
            return method_body.format(put_method="")

    def generateDeleteMethod(self, template):
        method_body = "public function delete($request) {{ {delete_method} }}"

        if self.evaluatesToTrue(self.delete):
            return method_body.format(delete_method="$id = $this->filterParameters(array('id'), $request->parameters);$this->getModel()->delete($this->formatParameters($id));")
        else:
            return method_body.format(delete_method="")

    def generate(self):
        with open('generators/controller_template.txt', 'r') as controller_template:
            data = controller_template.read()

            controller_name = self.construct_controller_name()
            post_method = self.generatePostMethod(data)
            put_method = self.generatePutMethod(data)
            delete_method = self.generateDeleteMethod(data)

            data = data.format(name=controller_name, post_method=post_method, put_method=put_method, delete_method=delete_method)

            with open('php/' + controller_name + '.php', 'w') as controller_file:
                controller_file.write(data)
