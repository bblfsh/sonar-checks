import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    cl_nodes = bblfsh.filter(uast, "//SynchronizedStatement/MethodInvocation"
            "/ThisExpression/parent::MethodInvocation/Identifier[@Name='getClass']")

    for node in cl_nodes:
        findings.append({"msg": "Don't use this.getClass() to synchronize, use MyClass.class",
            "pos": node.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
