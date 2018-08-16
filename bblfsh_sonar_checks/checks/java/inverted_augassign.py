# check: https://rules.sonarsource.c../../java/RSPEC-2757
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/inverted_augassign.java").uast

unary_repeated = bblfsh.filter(uast, "//*[@roleOperator and @token='=' and @internalRole='operator']/parent::*/"
        "/*[@internalRole='rightHandSide']/*[@internalRole='operator' and @roleOperator]/parent::*")

for ur in unary_repeated:
    print("Don't repeat Unary operators, line {}".format(ur.start_position.line))
