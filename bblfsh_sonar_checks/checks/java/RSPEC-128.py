import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    switches = bblfsh.filter(uast, "//SwitchStatement")
    for i in switches:
        cases = bblfsh.filter(i, "//SwitchCase")

        for c in cases:
            breaks = bblfsh.filter(c, "//*[@roleCase and @roleBreak]")
            if len(list(breaks)) == 0:
                findings.append({"msg": "Switch without break",
                                 "pos": c.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
