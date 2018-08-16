import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    usages = utils.instanced_calls(uast, "Thread", "run")
    for u in usages:
        findings.append({"msg": "Don't call run on Thread instances, use start() instead, line: {}",
                         "pos": u.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
