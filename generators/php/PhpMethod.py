class PhpMethod():

    def __init__(self, method_signature, method_body):
        self.method_signature = method_signature
        self.method_body = method_body

        self.method_skeleton = method_signature + " {{{body}}}" 
        self.complete_method = self.method_skeleton.format(body=method_body)

    def retrieve(self):
        return self.complete_method


