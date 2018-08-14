# check: https://rules.sonarsource.c../../java/RSPEC-2692
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/indexof_positive.java").uast
comps = bblfsh.filter(uast, "//InfixExpression[@roleGreaterThan]")

for comp in comps:
    m = bblfsh.filter(comp, "//MethodInvocation//Identifier[@Name='indexOf']")
    for idx_call in m:
        rights = bblfsh.filter(comp, "//NumberLiteral[@internalRole='rightOperand' and @token='0']")
        for r in rights:
            print("indexOf greater than zero ignores the first field at line {}"
                    .format(r.start_position.line));
