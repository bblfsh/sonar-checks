# check: https://rules.sonarsource.com/java/RSPEC-1214
import utils

import bblfsh

client = bblfsh.BblfshClient("0.0.0.0:9432")

uast = client.parse("../java/interface_constants.java").uast

cl_nodes = bblfsh.filter(uast, "//TypeDeclaration[@interface='true']/FieldDeclaration")

for cl in cl_nodes:
    print("Interface should not define a constant (line {})".format(cl.start_position.line))
