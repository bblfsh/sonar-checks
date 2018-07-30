import bblfsh

class Argument:
    def __init__(self, node):
        self.name = ''
        self.init = None
        self.type_ = None
        self.type_name = ''
        self.variadic = node.properties['Variadic'] == 'true'
        self.map_variadic = node.properties['MapVariadic'] == 'true'
        self.receiver = node.properties['Receiver'] == 'true'

        for c in node.children:
            if c.properties["internalRole"] == "Init":
                self.init = c
            elif c.properties["internalRole"] == "Type":
                self.type_ = c
                types = list(bblfsh.filter(node, "//Identifier"))
                if types:
                    self.type_name = types[0].properties['Name']
                else:
                    try:
                        self.type_name = node.children[0].token
                    except ValueError:
                        self.type_name = ''



class Method:
    def __init__(self, node):
        nodes = node.children
        self.modifiers = []
        self.arguments = []
        self.name = ''
        self.return_ = None

        for node in nodes:
            if node.internal_type == "Alias":

                for c in node.children:
                    if c.internal_type == "Identifier":
                        self.name = c.properties["Name"]

                    elif c.internal_type == "Function":

                        for fc in c.children:
                            if fc.internal_type == "FunctionType":

                                for ftc in fc.children:
                                    if ftc.properties["internalRole"] == "Returns":
                                        self.return_ = Argument(ftc)

                                    elif ftc.properties["internalRole"] == "Arguments":
                                        self.arguments.append(Argument(ftc))

                            elif fc.internal_type == "Block":
                                self.body = fc

            elif node.internal_type == "Modifier":
                self.modifiers.append(node.token)


class JClass:
    def __init__(self, node):
        self.name = ''
        self.methods = []
        self.fields = []
        self.parent = ''
        self.implements = []

        for c in node.children:
            if c.properties["internalRole"] == "name":
                self.name = c.properties["Name"]

            elif c.properties["internalRole"] == "superclassType":
                names = bblfsh.filter(c, "//Identifier")
                self.parent = '.'.join([i.properties["Name"] for i in names])

            elif c.properties["internalRole"] == "superInterfaceTypes":
                for iface in c.children:
                    names = bblfsh.filter(iface, "//Identifier")
                    names_qualified = '.'.join([i.properties["Name"] for i in names])
                    self.implements.append(names_qualified)

            elif c.properties["internalRole"] == "bodyDeclarations":
                    names = bblfsh.filter(c, "//FieldDeclaration/VariableDeclarationFragment//Identifier")
                    names_qualified = '.'.join([i.properties["Name"] for i in names])
                    self.fields.append(names_qualified)

        self.methods = get_methods(node)


def get_methods(node):
    return [Method(i) for i in bblfsh.filter(node, "//TypeDeclaration//FunctionGroup")]
