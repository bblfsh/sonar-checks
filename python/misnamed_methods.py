# check: https://rules.sonarsource.com/java/RSPEC-1221
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/misnamed_methods.java").uast
bad_methods = (
        ('hashcode', 'int', 'hashCode'),
        ('tostring', 'String', 'toString'),
        ('equal', 'boolean', 'equals'),
)

for method in utils.get_methods(uast):
    if "public" not in method.modifiers:
        continue

    for tup in bad_methods:
        if method.name == tup[0] and method.return_.type_name == tup[1]:
            print("Probably misnamed method '{}' instead of '{}' at line {}"
                .format(method.name, tup[2], method.node.start_position.line))
