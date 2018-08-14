# check: https://rules.sonarsource.c../../java/RSPEC-2225
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../../java/tostring_notnull.java").uast

def returnsNull(node):
    return any(list(bblfsh.filter(node, "//*[@roleReturn]//*[@roleNull]")))

methods = utils.get_methods(uast)

for m in methods:
    if (m.name == "toString" and "public" in m.modifiers and m.return_.type_name == "String"
           and not m.arguments) or\
       (m.name == "clone" and "public" in m.modifiers and m.return_.type_name == "Object"
           and not m.arguments):
        if returnsNull(m.node):
            print("Don't return Null on toString or clone methods, line {}"
                    .format(m.node.start_position.line))
