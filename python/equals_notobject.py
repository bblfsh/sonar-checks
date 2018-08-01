# check: https://rules.sonarsource.com/java/RSPEC-1201
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/equals_notobject.java").uast
methods = utils.get_methods(uast)

for m in methods:
    if m.name == "equals" and m.return_.type_name == "boolean" and \
            "public" in m.modifiers:
        args = m.arguments
        if len(args) != 1:
            print("equals method should have only one Object argument, line {}"
                    .format(m.node.start_position.line))

        if args[0].type_name != "Object":
            print("equals should be declared with an argument of type Object, line {}"
                    .format(m.node.start_position.line))
