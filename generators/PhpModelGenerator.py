
import os 
from abc import ABCMeta, abstractmethod
from generators.PhpGenerator import PhpGenerator
from generators.PhpMethod import PhpMethod

class PhpModelGenerator(PhpGenerator):

    def __init__(self, table_name, plural, post, put, delete):
        super().__init__(table_name, plural, post, put, delete)
        self.construct_method_signatures_and_bodies()

    def construct_method_signatures_and_bodies(self):
        base_method_signature = "public function {request_type}($request)"

        self.post_method_signature = base_method_signature.format(request_type="post")
        self.put_method_signature = base_method_signature.format(request_type="put")
        self.delete_method_signature = base_method_signature.format(request_type="delete")

        self.post_method_body = "$this->getModel()->insert($request->parameters);" if self.post else self.unimplementedMethodPlaceholder
        self.put_method_body = "\n\t\t$id = $request->parameters['id'];\n\t\t$primaryKey = 'id = $id';\n\t\tunset($request->parameters['id']);\n\t\t$this->getModel()->update($primaryKey, $request->parameters);\n\t" if self.put else self.unimplementedMethodPlaceholder
        self.delete_method_body = "$id = $this->filterParameters(array('id'), $request->parameters);$this->getModel()->delete($this->formatParameters($id));" if self.delete else self.unimplementedMethodPlaceholder

    def generate(self):
        with open('generators/controller_template.txt', 'r') as controller_template:
            data = controller_template.read()

            class_name = self.construct_name('Controller')
            post_method = PhpMethod(self.post_method_signature, self.post_method_body)
            put_method = PhpMethod(self.put_method_signature, self.put_method_body)
            delete_method = PhpMethod(self.delete_method_signature, self.delete_method_body)

            data = data.format(name=class_name, post_method=post_method.retrieve(), put_method=put_method.retrieve(), delete_method=delete_method.retrieve())

            os.makedirs('php/controllers/', exist_ok=True)

            with open('php/controllers/' + class_name + '.php', 'w') as controller_file:
                controller_file.write(data)

