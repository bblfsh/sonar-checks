import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []

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
            findings.append({"msg": "Loop variable {} modified".format(forVar),
                             "pos": p.start_position})

        prefixIds = bblfsh.filter(fn, "//Block//PrefixExpression/Identifier[@Name='{}']".format(forVar))
        for p in prefixIds:
            findings.append({"msg": "Loop variable {} modified".format(forVar),
                             "pos": p.start_position})

        assignIds = bblfsh.filter(fn, "//Block//Assignment//Identifier[@internalRole='leftHandSide' "
                                      "and @Name='{}']".format(forVar))
        for identifier in assignIds:
            findings.append({"msg": "Loop variable {} modified".format(forVar),
                             "pos": identifier.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
