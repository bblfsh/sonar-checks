import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    cl_nodes = bblfsh.filter(uast, "//*[@roleDeclaration and @roleType]")

    for cl in cl_nodes:
        jc = utils.JClass(cl)
        if jc.parent.split('.')[-1] == jc.name:
            findings.append({"msg": 'Class has same name as parent'})

        for impl in jc.implements:
            if impl.split('.')[-1] == jc.name:
                findings.append({"msg": 'Class has same name as interface'})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
