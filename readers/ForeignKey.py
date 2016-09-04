import re


class ForeignKey():

    def __init__(self, foreign_key):
        self.key = foreign_key['key']
        self.reference = foreign_key['reference']

        pattern = "(.*)\((.*)\)"
        match = re.search(pattern, foreign_key['reference'])

        if match:
            self.foreign_table = match.group(1)
            self.foreign_column = match.group(2)
