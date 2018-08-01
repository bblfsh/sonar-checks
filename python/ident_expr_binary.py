# check: https://rules.sonarsource.com/java/RSPEC-1764
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/ident_expr_binary.java").uast

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
        print("Equal terms on both sides of binary expression, line: {}"
                .format(node.start_position.line))
