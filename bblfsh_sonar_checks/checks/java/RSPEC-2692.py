import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

    comps = bblfsh.filter(uast, "//InfixExpression[@roleGreaterThan]")

    for comp in comps:
        m = bblfsh.filter(comp, "//MethodInvocation//Identifier[@Name='indexOf']")
        for idx_call in m:
            rights = bblfsh.filter(comp, "//NumberLiteral[@internalRole='rightOperand' and @token='0']")
            for r in rights:
                findings.append({"msg": "indexOf greater than zero ignores the first field",
                                 "pos": r.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
