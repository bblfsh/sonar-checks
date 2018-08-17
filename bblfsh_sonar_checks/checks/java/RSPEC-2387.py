import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    classes = []
    name2class = {}

    cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")

    for cl in cl_nodes:
        jc = utils.JClass(cl)
        name2class[jc.name] = jc

    for clname, cl in name2class.items():
        if not cl.parent:
            continue

        parent = name2class.get(cl.parent)
        if not parent:
            continue

        common = set([i.name for i in cl.fields]) & set([i.name for i in parent.fields])
        if len(common):
            findings.append({"msg": 'Class {} uses field(s) with same name as parent {}: {}'.format(
                cl.name, parent.name, common)})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
