import bblfsh

class Argument:
    def __init__(self, node):
        self.init = None
        self.type_ = None
        self.type_name = ''
        self.name = ''
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
            elif c.properties["internalRole"] == "Name":
                self.name = c.properties["Name"]

class Method:
    def __init__(self, node):
        self.node = node
        self.modifiers = []
        self.arguments = []
        self.name = ''
        self.return_ = None
        self.body = None

        for node in node.children:
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

class JClassField:
    def __init__(self, node):
        self.name = ''
        self.node = node
        self.modifiers = []
        self.type_name = ''

        name_node = list(bblfsh.filter(node, "//VariableDeclarationFragment/Identifier"))[0]
        self.name = name_node.properties["Name"]

        modifier_nodes = bblfsh.filter(node, "//Modifier")
        for m in modifier_nodes:
            self.modifiers.append(m.token)

        type_node = list(bblfsh.filter(node, "//*[@roleType]"))[0]
        if type_node.internal_type == "SimpleType":
            self.type_name = list(bblfsh.filter(type_node, "//Identifier"))[0].properties["Name"]


class JClass:
    def __init__(self, node):
        self.name = ''
        self.methods = []
        self.parent = ''
        self.implements = []
        self.node = node

        fields = bblfsh.filter(node, "//FieldDeclaration")
        self.fields = [JClassField(i) for i in fields]

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

            # elif c.properties["internalRole"] == "bodyDeclarations":
                    # names = bblfsh.filter(c, "//FieldDeclaration/VariableDeclarationFragment//Identifier")
                    # names_qualified = '.'.join([i.properties["Name"] for i in names])
                    # self.fields.append(names_qualified)

        self.methods = get_methods(node)


def get_methods(node):
    return [Method(i) for i in bblfsh.filter(node, "//TypeDeclaration//FunctionGroup")]


def hash_node(node, ignore_sideness=True):
    """ Hashes a node ignoring positional information """
    import hashlib

    lroles = [str(i) for i in node.roles if i not in (bblfsh.role_id("LEFT"),
                bblfsh.role_id("RIGHT"))]

    hash = hashlib.md5()
    stuff = [node.internal_type, node.token] + lroles

    for prop, value in sorted(node.properties.items()):
        if ignore_sideness and 'left' in value.lower() or 'right' in value.lower():
            continue
        stuff.append(prop)
        stuff.append(value)

    child_hashes = []
    for child in node.children:
        child_hashes.append(hash_node(child, ignore_sideness)
                            .hexdigest().encode('utf-8'))

    stuff.extend(sorted(child_hashes))

    for s in stuff:
        hash.update(str(s).encode('utf-8'))

    return hash
