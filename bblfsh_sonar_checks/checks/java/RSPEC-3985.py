import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    for cl in [utils.JClass(i) for i in bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")]:
        instance_creations = bblfsh.filter(cl.node, "//ClassInstanceCreation/SimpleType/Identifier")
        all_creations = {i.properties["Name"] for i in instance_creations}

        for cls in [utils.JClass(i) for i in
                bblfsh.filter(cl.node, "//TypeDeclaration//TypeDeclaration")]:
            for child in cls.node.children:
                if child.internal_type == "Modifier" and child.token == "private" and\
                    cls.name not in all_creations:
                    findings.append({"msg": "Private class {} defined but not used, remove it".format(cls.name),
                        "pos": cls.node.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
