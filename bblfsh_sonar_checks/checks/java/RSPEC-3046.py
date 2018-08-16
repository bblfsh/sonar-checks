import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    cl_nodes = bblfsh.filter(uast, "//SynchronizedStatement//SynchronizedStatement//"
                                   "MethodInvocation//Identifier[@Name='wait']")

    for node in cl_nodes:
        findings.append({"msg": "Don't call wait with more than one concurrent lock held",
            "pos": node.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
