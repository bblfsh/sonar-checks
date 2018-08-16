import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    and_minusone = bblfsh.filter(uast, "//PrefixExpression[@roleUnary and @roleOperator and @roleNegative and @roleRight]/"
                                       "NumberLiteral[@internalRole='operand' and @token='1']/"
                                       "parent::PrefixExpression/parent::InfixExpression[@roleBitwise and @roleAnd]")
    for am in and_minusone:
        findings.append({"msg": "Binary and (&) with '-1' always give the original value",
                         "pos": am.start_position})

    xor_zero = bblfsh.filter(uast, "//InfixExpression[@roleBinary and @roleXor]/"
                                   "NumberLiteral[@roleRight and @token='0']")

    for xz in xor_zero:
        findings.append({"msg": "Binary xor (^) with '0' always give the original value",
                         "pos": xz.start_position})

    or_zero = bblfsh.filter(uast, "//InfixExpression[@roleBinary and @roleBitwise and @roleOr]/"
                                  "NumberLiteral[@roleRight and @token='0']")

    for oz in or_zero:
        findings.append({"msg": "Binary or (|) with '0' always give the original value",
                         "pos": oz.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
