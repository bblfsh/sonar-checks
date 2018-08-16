import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    switches = bblfsh.filter(uast, "//SwitchStatement")
    for i in switches:
        cases = list(bblfsh.filter(i, "//SwitchCase"))
        if not cases:
            continue

        for r in range(len(cases)):
            c = cases[r]
            if bblfsh.role_id('DEFAULT') in c.roles and r != (len(cases)-1):
                    findings.append({"msg": "'default' should be the line switch case",
                        "pos": c.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
