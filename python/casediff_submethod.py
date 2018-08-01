import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/casediff_submethod.java").uast
classes = []
name2class = {}

cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")

for cl in cl_nodes:
    jc = utils.JClass(cl)
    name2class[jc.name] = jc

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
