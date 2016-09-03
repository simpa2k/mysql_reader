class MethodFormatter():

    def __init__(self):
        self.tokens = {
                '{': {"indents": 1},
                '}': {"indents": -1},
                ';': {"indents": 0}
                }
    
    def insertTabs(self, tabs, indents):
        for i in range(indents):
            tabs += "\t"

        return tabs

    def deleteTabs(self, tabs, dedents):
        for i in range(0, dedents, -1):
            tabs = tabs[: len(tabs) - 1]

        return tabs

    def prettify(self, method):
        
        prettifiedMethod = ""

        tabs = "\t"
        for i, c in enumerate(method):
            if i + 1 < len(method):
                next = method[i + 1]
                if next in self.tokens and self.tokens[next]["indents"] < 0:
                    tabs = self.deleteTabs(tabs, self.tokens[next]["indents"])
                    prettifiedMethod += c + "\n" + tabs.expandtabs(4)
                elif c in self.tokens and self.tokens[c]["indents"] >= 0:
                    tabs = self.insertTabs(tabs, self.tokens[c]["indents"])
                    prettifiedMethod += c + "\n" + tabs.expandtabs(4)
                else:
                    prettifiedMethod += c
            else: prettifiedMethod += c

        return prettifiedMethod 
            
