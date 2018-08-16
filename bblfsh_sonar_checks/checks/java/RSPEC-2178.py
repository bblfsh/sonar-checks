import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    ifs = bblfsh.filter(uast, "//*[@roleBitwise and @roleCondition and @roleIf]")

    if len(list(ifs)) > 0:
        findings.append({"msg": "Potential bug: bitwise operator inside if condition"})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
