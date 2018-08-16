import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    cl_nodes = bblfsh.filter(uast, "//TypeDeclaration[@interface='true']/FieldDeclaration")

    for cl in cl_nodes:
        findings.append({"msg": "Interface should not define a constant",
                         "pos": cl.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
