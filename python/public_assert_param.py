# check: https://rules.sonarsource.com/java/RSPEC-4274
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/public_assert_param.java").uast
methods = utils.get_methods(uast)

for m in methods:
    if "public" not in m.modifiers:
        continue

    for arg in m.arguments:
        for a in bblfsh.filter(m.node, "//AssertStatement//Identifier[@Name='%s']"
                                        % arg.name):
            print("Don't use asserts with public method parameters, line: {}".format(
                a.start_position.line))
