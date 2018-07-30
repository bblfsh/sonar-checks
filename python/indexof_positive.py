import utils

import bblfsh

if __name__ == '__main__':
    client = bblfsh.BblfshClient("0.0.0.0:9432")

    uast = client.parse("../java/indexof_positive.java").uast
    comps = bblfsh.filter(uast, "//InfixExpression[@roleGreaterThan]")

    for comp in comps:
        mi = bblfsh.filter(comp, "//MethodInvocation")
        m = bblfsh.filter(comp, "//MethodInvocation//Identifier[@Name='indexOf']")
        for idx_call in m:
            rights = bblfsh.filter(comp, "//NumberLiteral[@token='0']")
            for r in rights:
                if r.properties["internalRole"] == "rightOperand":
                    print("indexOf greater than zero ignores the first field");

