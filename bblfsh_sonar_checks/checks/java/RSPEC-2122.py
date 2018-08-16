import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    inst = bblfsh.filter(uast, "//ClassInstanceCreation/*[@internalRole='arguments'"
            " and @roleNumber and @token='0']/parent::*//Identifier/"
            "parent::SimpleType[@roleCall and @roleCallee and @roleType]")

    for i in inst:
        findings.append({"msg": "Don't instantiate ScheduledThreadPoolExecutes with an argument of 0",
                         "pos": i.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
