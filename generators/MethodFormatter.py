class MethodFormatter:

    def __init__(self):
        self.tokens = {
                '{': {"indents": 1},
                '}': {"indents": -1},
                ';': {"indents": 0}
                }
    
    def insert_tabs(self, tabs, indents):
        for i in range(indents):
            tabs += "\t"

        return tabs

    def delete_tabs(self, tabs, dedents):
        for i in range(0, dedents, -1):
            tabs = tabs[: len(tabs) - 1]

        return tabs

    def prettify(self, method):
        
        prettified_method = ""

        tabs = "\t"
        for i, c in enumerate(method):
            if i + 1 < len(method):
                next = method[i + 1]
                if next in self.tokens and self.tokens[next]["indents"] < 0:
                    tabs = self.delete_tabs(tabs, self.tokens[next]["indents"])
                    prettified_method += c + "\n" + tabs.expandtabs(4)
                elif c in self.tokens and self.tokens[c]["indents"] >= 0:
                    tabs = self.insert_tabs(tabs, self.tokens[c]["indents"])
                    prettified_method += c + "\n" + tabs.expandtabs(4)
                else:
                    prettified_method += c
            else: prettified_method += c

        return prettified_method
            
