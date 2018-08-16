import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    switches = bblfsh.filter(uast, "//SwitchStatement")
    for i in switches:
        cases = bblfsh.filter(i, "//SwitchCase")

        for c in cases:
            if bblfsh.role_id("DEFAULT") in c.roles:
                break
        else:
            findings.append({"msg": "Switch without default case",
                             "pos": i.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
