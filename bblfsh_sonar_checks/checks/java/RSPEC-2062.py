import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    cl_nodes = bblfsh.filter(uast, "//TypeDeclaration[@roleDeclaration and @roleType]//SimpleType"
            "[@internalRole='superInterfaceTypes']//Identifier[@Name='Serializable']/"
            "parent::*/parent::TypeDeclaration")

    for cl in cl_nodes:
        jc = utils.JClass(cl)

        for method in jc.methods:
            if method.name == 'readResolve' and 'private' in method.modifiers and\
                    method.return_ and method.return_.type_name == 'Object' and\
                    not method.arguments:
                findings.append({"msg": "Class {} implementing Serializable should have a public or protested "
                        "readResolve() method".format(jc.name),
                                 "pos": cl.start_position})
            break
        else:
            findings.append({"msg": "Class {} implementing Serializable should have a readResolve() method".format(jc.name),
                             "pos": cl.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
