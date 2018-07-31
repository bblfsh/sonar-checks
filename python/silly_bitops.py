# check: https://rules.sonarsource.com/java/RSPEC-2437
import utils

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/silly_bitops.java").uast

    and_minusone = bblfsh.filter(uast, "//PrefixExpression[@roleUnary and @roleOperator and @roleNegative and @roleRight]/"
                                       "NumberLiteral[@internalRole='operand' and @token='1']/"
                                       "parent::PrefixExpression/parent::InfixExpression[@roleBitwise and @roleAnd]")
    for am in and_minusone:
        print("Binary and (&) with '-1' always give the original value (line {})"
                .format(am.start_position.line))

    xor_zero = bblfsh.filter(uast, "//InfixExpression[@roleBinary and @roleXor]/"
                                   "NumberLiteral[@roleRight and @token='0']")

    for xz in xor_zero:
        print("Binary xor (^) with '0' always give the original value (line {})"
                .format(xz.start_position.line))

    or_zero = bblfsh.filter(uast, "//InfixExpression[@roleBinary and @roleBitwise and @roleOr]/"
                                  "NumberLiteral[@roleRight and @token='0']")

    for oz in or_zero:
        print("Binary or (|) with '0' always give the original value (line {})"
                .format(oz.start_position.line))
