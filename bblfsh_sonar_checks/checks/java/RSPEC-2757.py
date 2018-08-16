import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    unary_repeated = bblfsh.filter(uast, "//*[@roleOperator and @token='=' and @internalRole='operator']/parent::*/"
            "/*[@internalRole='rightHandSide']/*[@internalRole='operator' and @roleOperator]/parent::*")

    for ur in unary_repeated:
        findings.append({"msg": "Don't repeat Unary operators",
            "pos": ur.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
