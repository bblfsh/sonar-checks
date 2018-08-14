# check: https://rules.sonarsource.c../../java/RSPEC-1994
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/for_loopvar_modify.java").uast
for_nodes = bblfsh.filter(uast, "//ForStatement")

forVar = None

for fn in for_nodes:
    # Get the loop var
    for fc in fn.children:
        if fc.properties["internalRole"] == "expression":
            ids = bblfsh.filter(fc, "//Identifier")

            for i in ids:
                if i.properties["internalRole"] == "leftOperand":
                    forVar = i.properties["Name"]
                    break

    # Search for Assign / Postfix / Prefix exprs inside the for body
    postfixIds = bblfsh.filter(fn, "//Block//PostfixExpression/Identifier[@Name='{}']".format(forVar))
    for p in postfixIds:
        print("Loop variable {} modified at line {}".format(forVar, p.start_position.line))

    prefixIds = bblfsh.filter(fn, "//Block//PrefixExpression/Identifier[@Name='{}']".format(forVar))
    for p in prefixIds:
        print("Loop variable {} modified at line {}".format(forVar, p.start_position.line))

    assignIds = bblfsh.filter(fn, "//Block//Assignment//Identifier[@internalRole='leftHandSide' "
                                  "and @Name='{}']".format(forVar))
    for identifier in assignIds:
        print("Loop variable {} modified at line {}".format(forVar, identifier.start_position.line))
