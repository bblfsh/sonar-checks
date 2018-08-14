# check: https://rules.sonarsource.c../../java/RSPEC-2157
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/cloneable_without_clone.java").uast

cl_nodes = bblfsh.filter(uast, "//TypeDeclaration[@roleDeclaration and @roleType]//SimpleType"
        "[@internalRole='superInterfaceTypes']//Identifier[@Name='Cloneable']/"
        "parent::*/parent::TypeDeclaration")

for cl in cl_nodes:
    jc = utils.JClass(cl)

    for method in jc.methods:
        if method.name == 'clone' and 'public' in method.modifiers and\
                method.return_ and method.return_.type_name == 'Object' and\
                not method.arguments:
            break
    else:
        print("Class {} implementing Cloneable should have a clone() method (line {})"
                .format(jc.name, cl.start_position.line))
