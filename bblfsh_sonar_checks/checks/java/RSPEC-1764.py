import bblfsh_sonar_checks.utils as utils

import bblfsh

def check(uast):
    findings = []


    binexpr_nodes = bblfsh.filter(uast, "//InfixExpression[@roleBinary and @roleExpression]")

    for node in binexpr_nodes:
        left = None
        right = None

        for c in node.children:
            if bblfsh.role_id("LEFT") in c.roles:
                left = c

            elif bblfsh.role_id("RIGHT") in c.roles:
                right = c

            elif c.token in ["=", "*", "+"]:
                left = None
                right = None
                break

            if left and right:
                break

        if not left or not right:
            continue

        if utils.hash_node(left).hexdigest() == utils.hash_node(right).hexdigest():
            findings.append({"msg": "Equal terms on both sides of binary expression, ",
                             "pos": node.start_position})

    return findings

if __name__ == '__main__': utils.run_default_fixture(__file__, check)
