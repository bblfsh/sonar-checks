import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    cl_nodes = bblfsh.filter(uast, "//SynchronizedStatement//"
                                   "MethodInvocation/Identifier[@Name='sleep' and @roleCallee]/"
                                   "parent::MethodInvocation/Identifier[@Name='Thread' and @roleReceiver]")

    for node in cl_nodes:
        findings.append({"msg": "Don't call Thread.sleep() inside synchonized blocks, use wait instead",
                         "pos": node.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
