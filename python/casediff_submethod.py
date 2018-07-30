import utils

import bblfsh

class JavaClass:
    def __init__(self, name, methods, parent=None):
        self.name = name
        self.methods = methods
        self.parent = parent


if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/casediff_submethod.java").uast
    classes = []
    name2class = {}

    # Get the name, parent and methods of all classes
    cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")

    for cl in cl_nodes:
        name = ''
        parent_class = ''

        for c in cl.children:
            if c.properties["internalRole"] == "name":
                name = c.properties["Name"]

            elif c.properties["internalRole"] == "superclassType":
                parent_class = list(bblfsh.filter(c, "//Identifier"))[0].properties["Name"]

        name2class[name] = JavaClass(name, utils.get_methods(cl), parent_class)

    for clname, cl in name2class.items():
        if not cl.parent:
            continue

        methods = cl.methods
        for method in methods:
            for parmethod in name2class[cl.parent].methods:
                if parmethod.name != method.name and \
                   parmethod.name.lower() == method.name.lower():

                    print("Methods with same name but different casing in subclass: "
                          "{}.{} and {}.{}".format(clname, method.name, cl.parent, parmethod.name))
