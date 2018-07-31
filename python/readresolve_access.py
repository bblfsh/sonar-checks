# check: https://rules.sonarsource.com/java/RSPEC-2062
import utils

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/readresolve_access.java").uast

    cl_nodes = bblfsh.filter(uast, "//TypeDeclaration[@roleDeclaration and @roleType]//SimpleType"
            "[@internalRole='superInterfaceTypes']//Identifier[@Name='Serializable']/"
            "parent::*/parent::TypeDeclaration")

    for cl in cl_nodes:
        jc = utils.JClass(cl)

        for method in jc.methods:
            if method.name == 'readResolve' and 'private' in method.modifiers and\
                    method.return_ and method.return_.type_name == 'Object' and\
                    not method.arguments:
                print("Class {} implementing Serializable should have a public or protested "
                        "readResolve() method (line {})" .format(jc.name, cl.start_position.line))
            break
        else:
            print("Class {} implementing Serializable should have a readResolve() method (line {})"
                    .format(jc.name, cl.start_position.line))
