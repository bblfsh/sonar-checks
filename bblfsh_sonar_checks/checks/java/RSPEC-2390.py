import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    classes = []
    parent2children = {}
    name2class = {}

    cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")

    for cl in cl_nodes:
        jc = utils.JClass(cl)
        name2class[jc.name] = jc

        if jc.parent in parent2children:
            parent2children[jc.parent].append(jc.name)
        else:
            parent2children[jc.name] = [jc.parent]

        classes.append(jc)
        name2class[jc.name] = cl


    for cl in parent2children:
        for child in parent2children[cl]:
            # Alternative: generate a string with all the child names in the Identifier selector
            child_cl = name2class.get(cl)
            if not child_cl:
                continue

            calls = bblfsh.filter(child_cl,
                    "(//MethodInvocation//Identifier[@roleCall and @roleReceiver and @Name='%s']|"
                    "//QualifiedIdentifier//Identifier[@Name='%s'])" % (child, child))

            for call in calls:
                findings.append({"msg": "Call in class {} to subclass {} member".format(cl, child),
                                 "pos": call.start_position.line})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
